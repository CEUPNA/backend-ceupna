# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (TIC, Center, Degree, Department, Event, Representative, Subject,
                     Teacher)

# Register your models here.

admin.site.register(Center)
admin.site.register(Degree)
admin.site.register(Department)
admin.site.register(Event)
#admin.site.register(Representative)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(TIC)


class RepresentativeDegreeInline(admin.TabularInline):
    model = Representative.degree.through
    #fields = '__all__'
    verbose_name = "titulación"
    verbose_name_plural = "titulaciones"
    extra = 0


@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    #exclude = ("degree",)
    inlines = (RepresentativeDegreeInline,)
