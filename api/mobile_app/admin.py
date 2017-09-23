# -*- coding: utf-8 -*-

from .models import Center, Degree, Subject, Teacher, TIC
from django.contrib import admin

# Register your models here.

admin.site.register(Center)
admin.site.register(Degree)
admin.site.register(TIC)
admin.site.register(Subject)
admin.site.register(Teacher)