# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

LANGUAGES = [('es', 'Español'), ('en', 'Inglés'), ('eus', 'Euskera'), ('fr', 'Francés')]
TYPE_SUBJ = [('ba', 'Básica'), ('ob', 'Obligatoria'), ('op', 'Optativa')]
TYPE_RULES = [('ens', 'Enseñanzas'), ('est', 'Estudiantes'), ('gen', 'General')]
EVENT_SCHEDULE = [('inst', 'Institucional'), ('ceupna', 'Consejo de Estudiantes')]
EVENT_TAG = [('ens', 'Enseñanzas'), ('est', 'Estudiantes'), ('gen', 'General')]
SEX = [('h', 'Hombre'), ('m', 'Mujer')]
YEAR = [('1', 'Primero'), ('2', 'Segundo'), ('3', 'Tercero'), ('4', 'Cuarto'), ('5', 'Quinto'), ('6', 'Sexto')]


class HistoryRelation(models.Model):
    """
    Clase abstracta para manejar los historiales
    """
    init_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    def clean(self, *args, **kwargs):
        if self.end_date and self.init_date > self.end_date:
            raise ValidationError('La fecha de comienzo debe ser anterior a la de final.')
        super(HistoryRelation, self).clean(*args, **kwargs)

    class Meta:
        abstract = True


class Institution(models.Model):
    """
    Clase para la representación de un órgano de la Universidad
    """
    created = models.DateTimeField(auto_now_add=True)
    name_es = models.CharField(max_length=100, blank=True, default='')
    name_eus = models.CharField(max_length=100, blank=True, default='')
    name_en = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    telephone = models.CharField(max_length=20, blank=True, default='')
    web = models.URLField(blank=True, default='')
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    def __str__(self):
        return self.name_es

    class Meta:
        abstract = True


class Department(Institution):
    """
    Clase para la representación de un departamento.
    """
    active = models.BooleanField(default=True)
    director = models.ForeignKey('Teacher', default=None, on_delete=models.CASCADE)
    number_representative_members = models.PositiveIntegerField(blank=True, default=0)
    representative_members = models.ManyToManyField('Representative', through='DepartmentRepresentative',
                                                    through_fields=('department', 'representative'),
                                                    related_name='department_representatives')

    class Meta:
        ordering = ('active', 'name_es',)
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'


class DepartmentRepresentative(HistoryRelation):
    representative = models.ForeignKey('Representative', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)


class Center(Institution):
    """
    Clase para la representación de un centro universitario.
    """
    center_id = models.PositiveIntegerField(unique=True)
    acronym = models.CharField(max_length=10, blank=True, default='')
    number_representative_members = models.PositiveIntegerField(blank=True, default=0)
    representative_members = models.ManyToManyField('Representative', through='CenterRepresentative',
                                                    through_fields=('center', 'representative'),
                                                    related_name='center_representatives')
    number_quality_representative_members = models.PositiveIntegerField(blank=True, default=0)
    quality_representative_members = models.ManyToManyField('Representative', through='CenterQualityRepresentative',
                                                            through_fields=('center', 'representative'),
                                                            related_name='quality_representatives')

    class Meta:
        ordering = ('created',)
        verbose_name = 'centro'
        verbose_name_plural = 'centros'


class CenterRepresentative(HistoryRelation):
    representative = models.ForeignKey('Representative', on_delete=models.CASCADE)
    center = models.ForeignKey('Center', on_delete=models.CASCADE)


class CenterQualityRepresentative(HistoryRelation):
    representative = models.ForeignKey('Representative', on_delete=models.CASCADE)
    center = models.ForeignKey('Center', on_delete=models.CASCADE)


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
    sex = models.CharField(max_length=1, blank=True, default='', choices=SEX)
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
    claustral = models.BooleanField(default=False)
    delegate = models.BooleanField(default=True)
    degree = models.ManyToManyField('Degree', through='RepresentativeDegree', through_fields=('representative', 'degree'))
    year = models.CharField(max_length=1, blank=True, default='', choices=YEAR)
    # Las relaciones con cada uno de los sitios donde es representantes vienen en los otros modelos.

    def __str__(self):
        return self.last_name.upper() + ', ' + self.first_name

    class Meta:
        ordering = ('-active', 'last_name', 'first_name')
        verbose_name = 'representante'
        verbose_name_plural = 'representantes'


class RepresentativeDegree(HistoryRelation):
    representative = models.ForeignKey('Representative', on_delete=models.CASCADE)
    degree = models.ForeignKey('Degree', on_delete=models.CASCADE)


class Rule(models.Model):
    """
    Clase para la representación de una normativa universitaria.
    """
    # En la vista habrá que preparar que se vela URL de la última versión.
    created = models.DateTimeField(auto_now_add=True)
    name_es = models.CharField(max_length=150, blank=True, default='')
    name_eus = models.CharField(max_length=150, blank=True, default='')
    name_en = models.CharField(max_length=150, blank=True, default='')
    rule_group = models.CharField(max_length=3, blank=True, default='', choices=TYPE_RULES)
    last_updated = models.DateTimeField(auto_now=True)  # Para saber cuando fue la última vez que se cambió.

    def __str__(self):
        return self.name_es

    class Meta:
        ordering = ('created',)
        verbose_name = 'normativa'
        verbose_name_plural = 'normativas'


class RuleVersion(models.Model):
    """
    Clase para la representación de una versión de una normativa universitaria.
    """
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True, default='')
    document = models.URLField(blank=True, default='')
    date = models.DateField(blank=True)
    rule = models.ForeignKey('Rule', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('rule', 'created',)
        verbose_name = 'versión'
        verbose_name_plural = 'versiones'


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


class StudentCouncil(Institution):
    center = models.ForeignKey('Center', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('center', 'created',)
        verbose_name = 'Consejo de Estudiantes'
        verbose_name_plural = 'Consejos de Estudiantes'


class Responsibility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name_es = models.CharField(max_length=100, blank=True, default='')
    name_eus = models.CharField(max_length=100, blank=True, default='')
    name_en = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(blank=True)
    student_council = models.ForeignKey('StudentCouncil', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    representative = models.ManyToManyField('Representative', through='ResponsibilityRepresentativeHistory',
                                                    through_fields=('responsibility', 'representative'),
                                                    related_name='responsibility_representatives',
                                                    related_query_name='rres')

    def __str__(self):
        return self.name_es + ' (' + self.student_council.name_es + ')'


class ResponsibilityRepresentativeHistory(HistoryRelation):
    representative = models.ForeignKey('Representative', on_delete=models.CASCADE)
    responsibility = models.ForeignKey('Responsibility', on_delete=models.CASCADE)

    def __str__(self):
        return self.representative.__str__()


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
        ordering = ('first_name', 'created',)
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
