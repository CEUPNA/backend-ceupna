# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (TIC, Center, Degree, Event, Representative, Subject,
                     Teacher)

# Register your models here.

admin.site.register(Center)
admin.site.register(Degree)
admin.site.register(Event)
admin.site.register(TIC)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Representative)
