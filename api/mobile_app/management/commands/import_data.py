import json

from django.core.management.base import BaseCommand, CommandError
from mobile_app.models import Teacher


class Command(BaseCommand):
    help = 'Importación de los datos de la araña'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help="Archivo JSON con todos los datos de los profesores.")

    def handle(self, *args, **options):
        try:
            with open(options.get('file', ''), 'r') as f:
                data = json.load(f)
        except IOError:
            self.stderr.write("Archivo '%s' no encontrado" % options.get('file', ''))
            raise CommandError("Indique un archivo correcto para poder continuar. Ejecutar de nuevo el comando.")
            # return

        self._parse_teachers_file(data)
        self.stdout.write("Datos incluidos de forma adecuada.")

    @staticmethod
    def _parse_teachers_file(teachers_data):
        # TODO: Hacer algo para comprobar que el formato de los JSON está bien generado.

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

            max_char = 0
            if max_char < t['timetable'].__len__():
                max_char = t['timetable'].__len__()

            print(t['timetable'].__len__())
            teacher.save()

        print(max_char)
