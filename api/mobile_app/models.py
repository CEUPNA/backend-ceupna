# -*- coding: utf-8 -*-

from django.db import models

LANGUAGES = ['es', 'en', 'eus', 'fr']


class Center(models.Model):
    """
    Clase para la representación de un centro universitario.
    """
    created = models.DateTimeField(auto_now_add=True)
    center_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True, default='')
    acronym = models.CharField(max_length=10, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    telephone = models.CharField(max_length=20, blank=True, default='')
    url = models.URLField(blank=True, default='')
    last_updated = models.DateField(auto_now=True)  # Para saber cuándo fue la última vez que se cambió.

    class Meta:
        ordering = ('created',)


class Teacher(models.Model):
    """
    Clase para la representación de un profesor.
    """
    created = models.DateTimeField(auto_now_add=True)
    upna_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='', unique=True)
    telephone = models.CharField(max_length=20, blank=True, default='')
    timetable = models.TextField(max_length=100000, blank=True, default='')  # TODO: Hacer algo con la longitud.
    # subjects. Será una clave extranjera de la tabla de asignaturas.
    last_updated = models.DateField(auto_now=True)  # Para saber cuándo fue la última vez que se cambió.

    class Meta:
        ordering = ('created',)


class TIC(models.Model):
    """
    Clase para la representación de un recurso TIC.
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    icon = models.URLField(blank=True, default='')
    description = models.TextField(max_length=1000, blank=True, default='')
    url = models.URLField(blank=True, default='')
    last_updated = models.DateField(auto_now=True)  # Para saber cuándo fue la última vez que se cambió.

    class Meta:
        ordering = ('created',)
