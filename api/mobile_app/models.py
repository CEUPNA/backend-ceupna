# -*- coding: utf-8 -*-

from django.db import models

LANGUAGES = [('es', 'Español'), ('en', 'Inglés'), ('eus', 'Euskera'), ('fr', 'Francés')]
TYPE_SUBJ = [('ba', 'Básica'), ('ob', 'Obligatoria'), ('op', 'Optativa')]
EVENT_SCHEDULE = [('inst', 'Institucional'), ('ceupna', 'Consejo de Estudiantes')]
EVENT_TAG = [('ens', 'Enseñanzas'), ('est', 'Estudiantes'), ('gen', 'General')]


class Center(models.Model):
    """
    Clase para la representación de un centro universitario.
    """
    created = models.DateTimeField(auto_now_add=True)
    center_id = models.PositiveIntegerField(unique=True)
    name_es = models.CharField(max_length=100, blank=True, default='')
    name_eus = models.CharField(max_length=100, blank=True, default='')
    name_en = models.CharField(max_length=100, blank=True, default='')
    acronym = models.CharField(max_length=10, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    telephone = models.CharField(max_length=20, blank=True, default='')
    web = models.URLField(blank=True, default='')
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    def __str__(self):
        return self.name_es

    class Meta:
        ordering = ('created',)
        verbose_name = 'centro'
        verbose_name_plural = 'centros'


class Degree(models.Model):
    """
    Clase para la representación de un estudio de grado o máster.
    """
    created = models.DateTimeField(auto_now_add=True)
    upna_id = models.PositiveIntegerField()
    name_es = models.CharField(max_length=150, blank=True, default='')
    name_eus = models.CharField(max_length=150, blank=True, default='')
    name_en = models.CharField(max_length=150, blank=True, default='')
    language = models.CharField(max_length=3, blank=True, default='', choices=LANGUAGES)
    web = models.URLField(max_length=200, blank=True, default='')
    bachelor = models.BooleanField(default=False)
    international_prog = models.BooleanField(default=False)
    english_prog = models.BooleanField(default=False)
    french_prog = models.BooleanField(default=False)
    center = models.ManyToManyField('Center')
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    def clean(self):
        """
        Se encarga de sustituir cualquier dato del campo ´language´ a inglés si es un programa internacional.
        """
        if self.international_prog:
            self.language = 'en'

    def __str__(self):
        return self.name_es

    class Meta:
        ordering = ('upna_id',)
        unique_together = ('upna_id', 'language',)
        verbose_name = 'titulación'
        verbose_name_plural = 'titulaciones'


class Event(models.Model):
    """
    Clase para la representación de una actividad.
    """
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=200, blank=True, default='')
    ical_id = models.CharField(max_length=100, blank=True, default='')
    begin_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    description = models.TextField(blank=True, default='')
    schedule = models.CharField(max_length=6, blank=False, default='', choices=EVENT_SCHEDULE)
    tag = models.CharField(max_length=10, blank=True, default='', choices=EVENT_TAG)
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    def __str__(self):
        return self.name + ' - ' + self.begin_date.__str__() + ' - ' + self.end_date.__str__()

    class Meta:
        ordering = ('created',)
        verbose_name = 'actividad'
        verbose_name_plural = 'actividades'


class Person(models.Model):
    """
    Clase abstracta para la representación de una persona.
    """
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, blank=True, default='', verbose_name='Nombre')
    last_name = models.CharField(max_length=100, blank=True, default='', verbose_name='Apellidos')
    email = models.EmailField(max_length=150, blank=True, default='', unique=True)
    telephone = models.CharField(max_length=30, blank=True, default='')
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    class Meta:
        abstract = True


class Representative(Person):
    """
    Clase para la representación de un representante de estudiantes.
    """
    photo = models.ImageField(blank=True, upload_to='representatives')
    miaulario = models.CharField(max_length=100, blank=True, default='')
    active = models.BooleanField(default=True)
    #degree = models.ForeignKey('Degree', on_delete=models.CASCADE)  # TODO: ¿Y cuando ha tenido más de uno?
    # Relaciones con el CE, Centros y Departamentos

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    class Meta:
        ordering = ( 'created',)
        verbose_name = 'representante'
        verbose_name_plural = 'representantes'

class Subject(models.Model):
    """
    Clase para la representación de una asignatura de un cierto grado o máster.
    """
    created = models.DateTimeField(auto_now_add=True)
    upna_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100, blank=True, default='')
    credits = models.FloatField(default=0, blank=True, )
    year = models.IntegerField(default=0, blank=True, )
    semester = models.IntegerField(default=0, blank=True, )
    type = models.CharField(max_length=2, blank=True, default='', choices=TYPE_SUBJ)
    language = models.CharField(max_length=3, blank=True, default='', choices=LANGUAGES)
    department = models.CharField(max_length=100, blank=True,
                                  default='')  # A futuro tendrá que ser una clave extranjera.
    degree = models.ForeignKey('Degree', on_delete=models.CASCADE)  # TODO: a uno y solo a uno???
    teachers = models.ManyToManyField('Teacher')
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    # Campos de la ficha
    evaluation = models.TextField(max_length=10000, blank=True, default='')
    contents = models.TextField(max_length=10000, blank=True, default='')
    curriculum = models.TextField(max_length=10000, blank=True, default='')

    # Direcciones web generadas al vuelo.
    @property
    def web(self):  # Para el idioma igual que la web de la UPNA
        # return "http://www.unavarra.es/ficha-asignaturaDOA/?languageId=%d&codPlan=%d&codAsig=%d&anio=%d" \
        #        % (100000, self.degree.upna_id, self.upna_id, 2016)
        return "http://www.unavarra.es/ficha-asignaturaDOA/?codAsig=%d" \
               % (self.upna_id,)

    @property
    def bibliography(self):  # Para el idioma (por ahora a nivel app): &LANG=es-ES &LANG=eu-ES &LANG=en-US
        return "https://biblioteca.unavarra.es/abnetopac/abnetcl.cgi?ACC=DOSEARCH&xsqf99=%d*.t901." \
               % (self.upna_id,)

    def __str__(self):
        return str(self.upna_id) + ' ' + self.name

    class Meta:
        ordering = ('created',)
        unique_together = ('upna_id', 'language',)
        verbose_name = 'asignatura'
        verbose_name_plural = 'asignaturas'


class Teacher(Person):
    """
    Clase para la representación de un profesor.
    """
    upna_id = models.PositiveIntegerField(unique=True)
    timetable = models.TextField(blank=True, default='')

    @property
    def web(self):
        return "http://www.unavarra.es/pdi?uid=%d" % (self.upna_id,)

    # @property
    # def subjects(self):
    #     return self.subject_set

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ('created',)
        verbose_name = 'profesor'
        verbose_name_plural = 'profesores'


class TIC(models.Model):
    """
    Clase para la representación de un recurso TIC.
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    icon = models.URLField(blank=True, default='')
    description = models.TextField(max_length=1000, blank=True, default='')
    web = models.URLField(blank=True, default='')
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)
        verbose_name = 'TIC'
        verbose_name_plural = 'TIC'
