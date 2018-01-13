# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


admin.site.register(models.Degree)
admin.site.register(models.Event)
admin.site.register(models.Subject)
admin.site.register(models.Teacher)
admin.site.register(models.TIC)


class CenterRepresentativeInline(admin.TabularInline):
    model = models.Center.representative_members.through
    verbose_name = "representante en Junta"
    verbose_name_plural = "representantes en Junta"
    extra = 0


class CenterQualityRepresentativeInline(admin.TabularInline):
    model = models.Center.quality_representative_members.through
    verbose_name = "representante en C. de Calidad"
    verbose_name_plural = "representantes en C. de Calidad"
    extra = 0


@admin.register(models.Center)
class CenterAdmin(admin.ModelAdmin):
    inlines = (CenterRepresentativeInline, CenterQualityRepresentativeInline,)


class DeparmentRepresentativeInline(admin.TabularInline):
    model = models.Department.representative_members.through
    verbose_name = "representante en Junta"
    verbose_name_plural = "representantes en Junta"
    extra = 0


@admin.register(models.Department)
class RepresentativeAdmin(admin.ModelAdmin):
    inlines = (DeparmentRepresentativeInline,)


class RepresentativeDegreeInline(admin.TabularInline):
    model = models.Representative.degree.through
    verbose_name = "titulación"
    verbose_name_plural = "titulaciones"
    extra = 0


@admin.register(models.Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    inlines = (RepresentativeDegreeInline,)


class RuleVersionInline(admin.TabularInline):
    model = models.RuleVersion
    verbose_name = 'versión'
    verbose_name_plural = 'versiones'

@admin.register(models.Rule)
class RuleAdmin(admin.ModelAdmin):
    inlines = (RuleVersionInline,)
