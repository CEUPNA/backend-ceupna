# -*- coding: utf-8 -*-

from django.db import models


class Teacher(models.Model):
    """
    Clase para la representación de un profesor.
    """
    created = models.DateTimeField(auto_now_add=True)
    upna_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True, default='')
    # No tiene sentido utilizar el campo especial ya que sino puede dar una serie de errores que no nos interesa.
    # Al fin y al cabo, internamente será un campo de caracteres.
    email = models.CharField(max_length=100, blank=True, default='')
    telephone = models.CharField(max_length=20, blank=True, default='')
    timetable = models.CharField(max_length=10000, blank=True, default='')
    # subjects. Será una clave extranjera de la tabla de asignaturas.

    class Meta:
        ordering = ('created',)


class TIC(models.Model):
    """
    Clase para la representación de un recurso TIC.
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    icon = models.CharField(max_length=200, blank=True, default='')
    description = models.CharField(max_length=1000, blank=True, default='')
    link = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ('created',)
