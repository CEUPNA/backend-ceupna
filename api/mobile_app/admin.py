# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (TIC, Center, Degree, Department, Event, Representative, Subject,
                     Teacher)

# Register your models here.

admin.site.register(Center)
admin.site.register(Degree)
admin.site.register(Department)
admin.site.register(Event)
admin.site.register(Representative)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(TIC)
