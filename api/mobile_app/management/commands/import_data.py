# -*- coding: utf-8 -*-

import json

from ...models import Center, Teacher, TIC
from django.core.management.base import BaseCommand
#from mobile_app.models import Center, Teacher, TIC


class Command(BaseCommand):
    help = 'Importación de los datos para las arañas y los archivos JSON preparados.'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--centers', type=str, help="Opción para introducir el fichero con todos los centros")
        parser.add_argument('-T', '--teachers', type=str, help="Opción para introducir el fichero con todos los profesores")
        parser.add_argument('-t', '--tics', type=str, help="Opción para introducir el fichero con todos los recursos TIC")

    def handle(self, *args, **options):
        if options.get('centers'):
            self._parse_centers(options.get('centers'))
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
            center.name = c['name']
            center.acronym = c['acronym']
            center.email = c['email']
            center.telephone = c['telephone']
            center.url = c['url']

            center.save()

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
            self.stdout.write("Todo los profesores han sido actualizados de forma correcta.")

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
            tic.url = t['url']
