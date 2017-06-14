# -*- coding: utf-8 -*-

from .models import Center, Degree, Subject, TIC
from django.contrib import admin

# Register your models here.

admin.site.register(Center)
admin.site.register(Degree)
admin.site.register(TIC)
