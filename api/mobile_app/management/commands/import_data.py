# -*- coding: utf-8 -*-

import json
import warnings

from ...models import Center, Degree, Subject, Teacher, TIC
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importación de los datos para las arañas y los archivos JSON preparados.'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--centers', type=str, help="Opción para introducir el fichero con todos los centros")
        parser.add_argument('-T', '--teachers', type=str, help="Opción para introducir el fichero con todos los profesores")
        parser.add_argument('-t', '--tics', type=str, help="Opción para introducir el fichero con todos los recursos TIC")
        parser.add_argument('-d', '--degrees', type=str, help="Opción para introducir el fichero con todas las titulaciones (grado + máster)")
        parser.add_argument('-s', '--subjects', type=str, help="Opción para introducir el fichero con todas las asignaturas")

    def handle(self, *args, **options):
        if options.get('centers'):
            self._parse_centers(options.get('centers'))
        elif options.get('degrees'):
            self._parse_degrees(options.get('degrees'))
        elif options.get('subjects'):
            self._parse_subjects(options.get('subjects'))
        elif options.get('teachers'):
            self._parse_teachers(options.get('teachers'))
        elif options.get('tics'):
            self._parse_tics(options.get('tics'))

    def _return_json(self, file_str):
        try:
            with open(file_str, 'r') as f:
                data = json.load(f)
        except IOError:
            self.stderr.write("Archivo '%s' no encontrado" % file_str)
            return None
        return data

    def _parse_centers(self, route):
        # TODO: Actualizaciones.

        # Se crea el árbol JSON desde el fichero.
        centers_data = self._return_json(route)

        # Se va iterando sobre los elementos que se van encontrando entre los datos extraídos del JSON.
        for c in centers_data:
            # Si el profesor ya existe en la base de datos se obtiene el objeto relacionado.
            try:
                center = Center.objects.get(center_id=c['center_id'])
            # Si el profesor es nuevo, se crea un nuevo objeto para introducirlo en la BBDD.
            except Center.DoesNotExist:
                center = Center()
                center.center_id = c['center_id']

            # Se introducen los demás datos, sustituyendo siempre los anteriores.
            # TODO: Revisar qué hacer para las actualizaciones... no tiene sentido actualizar con datos que ya están.
            center.name_es = c['name_es']
            center.name_eus = c['name_eus']
            center.name_en = c['name_en']
            center.acronym = c['acronym']
            center.email = c['email']
            center.telephone = c['telephone']
            center.web = c['web']

            center.save()

        if not centers_data:
            self.stdout.write("No hay datos que incluir en el fichero que ha pasado.")

    def _parse_degrees(self, route):
        # TODO: Actualizaciones.

        # Se crea el árbol JSON desde el fichero.
        degrees_data = self._return_json(route)

        # Se va iterando sobre los elementos que se van encontrando entre los datos extraídos del JSON.
        for d in degrees_data:
            # Si la titulación ya existe en la base de datos se obtiene el objeto relacionado.
            try:
                degree = Degree.objects.get(upna_id=d['upna_id'], language=d['language'])
            # Si el grado es nuevo, se crea un nuevo objeto para introducirlo en la BBDD.
            except Degree.DoesNotExist:
                degree = Degree()
                degree.upna_id = d['upna_id']
                degree.language = d['language']

            # Se introducen los demás datos, sustituyendo siempre los anteriores.
            # TODO: Revisar qué hacer para las actualizaciones... no tiene sentido actualizar con datos que ya están.
            degree.name_es = d['name_es']
            degree.name_eus = d['name_eus']
            degree.name_en = d['name_en']
            degree.web = d['web']
            degree.bachelor = d['bachelor']
            degree.international_prog = d['international_prog']
            degree.english_prog = d['english_prog']
            degree.french_prog = d['french_prog']

            degree.center.clear()
            for c in d['center']:
                if c['center_id'] is None:
                    pass
                else:
                    try:
                        degree.center.add(Center.objects.get(center_id=c['center_id']))
                    except Center.DoesNotExist:
                        warnings.warn("No existe el centro en cuestión.")

            degree.save()

        if not degrees_data:
            self.stdout.write("No hay datos que incluir en el fichero que ha pasado.")

    def _parse_subjects(self, route):
        # TODO: Actualizaciones.

        # Se crea el árbol JSON desde el fichero.
        subjects_data = self._return_json(route)

        # Se va iterando sobre los elementos que se van encontrando entre los datos extraídos del JSON.
        for s in subjects_data:
            # Si la titulación ya existe en la base de datos se obtiene el objeto relacionado.
            try:
                subject = Subject.objects.get(upna_id=s['subject_id'])
            # Si el profesor es nuevo, se crea un nuevo objeto para introducirlo en la BBDD.
            except Subject.DoesNotExist:
                subject = Subject()
                subject.upna_id = s['subject_id']

            # Se introducen los demás datos, sustituyendo siempre los anteriores.
            # TODO: Revisar qué hacer para las actualizaciones... no tiene sentido actualizar con datos que ya están.
            if s['name'] is None:
                if subject.name is None:
                    subject.name = ""
            else:
                subject.name = s['name']

            if s['credits'] is None:
                if subject.credits is None:
                    subject.credits = 0
            else:
                subject.credits = s['credits']

            if s['semester'] is None:
                if subject.semester is None:
                    subject.semester = 0
            else:
                subject.semester = s['semester']

            if s['type'] is None:
                if subject.type is None:
                    subject.type = ""
            else:
                subject.type = s['type']

            subject.language = s['language']

            if s['department'] is None:
                if subject.department is None:
                    subject.department = ""
            else:
                subject.department = s['department']

            if s['year'] is None:
                if subject.year is None:
                    subject.year = 0
            else:
                subject.year = s['year']

            degree = None
            try:
                if s['degree_id'] is not None:
                    degree = Degree.objects.get(upna_id=s['degree_id'])
            except Degree.DoesNotExist:
                degree = None
                warnings.warn("La titulación que ha indicado para la asignatura %d no existe en la base de datos."
                              "Por favor, solucione este problema antes de introducir la asignatura." % subject.upna_id)
            subject.degree = degree

            subject.teachers.clear()
            if s['teachers'] is None:
                pass
            else:
                for t_id in s['teachers']:
                    try:
                        subject.teachers.add(Teacher.objects.get(upna_id=t_id))
                    except Teacher.DoesNotExist:
                        warnings.warn("No está el profesor en cuestión")

            if s['contents'] is None:
                if subject.contents is None:
                    subject.contents = ""
            else:
                subject.contents = s['contents']

            if s['curriculum'] is None:
                if subject.contents is None:
                    subject.curriculum = ""
            else:
                subject.curriculum = s['curriculum']

            if s['evaluation'] is None:
                if subject.evaluation is None:
                    subject.evaluation = ""
            else:
                subject.evaluation = s['evaluation']

            subject.save()

        if not subjects_data:
            self.stdout.write("No hay datos que incluir en el fichero que ha pasado.")

    def _parse_teachers(self, route):
        # TODO: Hacer algo para comprobar que el formato de los JSON está bien generado.

        # Se crea el árbol JSON desde el fichero.
        teachers_data = self._return_json(route)

        # Se va iterando sobre los elementos que se van encontrando entre los datos extraídos del JSON.
        for t in teachers_data:
            # Si el profesor ya existe en la base de datos se obtiene el objeto relacionado.
            try:
                teacher = Teacher.objects.get(upna_id=t['upna_id'])
            # Si el profesor es nuevo, se crea un nuevo objeto para introducirlo en la BBDD.
            except Teacher.DoesNotExist:
                teacher = Teacher()
                teacher.upna_id = t['upna_id']

            # Se introducen los demás datos, sustituyendo siempre los anteriores.
            # TODO: Revisar qué hacer para las actualizaciones... no tiene sentido actualizar con datos que ya están.
            teacher.name = t['name']
            teacher.email = t['email']
            teacher.telephone = t['telephone']
            teacher.timetable = t['timetable']

            if t['timetable'].__len__() > teacher.timetable.__len__():
                teacher.timetable = 'Por motivos técnicos no podemos motrar ahora esta información. Puedes comprobarlo'\
                                    + 'directamente en la <a href=\"http://www.unavarra.es/pdi?dato=tutorias&uid=' \
                                    + t['upna_id'] + '\">web de la universidad</a>.'

            teacher.save()
            # TODO: Incluir lo que tengo en producción

        if not teachers_data:
            self.stdout.write("No hay datos que incluir en el fichero que ha pasado.")

    def _parse_tics(self, route):
        # TODO: Actualizaciones

        # Se crea el árbol JSON desde el fichero.
        tics_data = self._return_json(route)

        # Se va iterando sobre los elementos que se van encontrando entre los datos extraídos del JSON.
        for t in tics_data:
            # Si el profesor ya existe en la base de datos se obtiene el objeto relacionado.
            try:
                tic = TIC.objects.get(id=t['id'])
            # Si el profesor es nuevo, se crea un nuevo objeto para introducirlo en la BBDD.
            except TIC.DoesNotExist:
                tic = TIC()

            # Se introducen los demás datos, sustituyendo siempre los anteriores.
            # TODO: Revisar qué hacer para las actualizaciones... no tiene sentido actualizar con datos que ya están.
            tic.name = t['name']
            tic.icon = t['icon']
            tic.description = t['description']
            tic.web = t['web']

            tic.save()

        if not tics_data:
            self.stdout.write("No hay datos que incluir en el fichero que ha pasado.")
