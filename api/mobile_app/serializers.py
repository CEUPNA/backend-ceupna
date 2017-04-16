# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Teacher, TIC


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'upna_id', 'name', 'email', 'telephone', 'timetable')


class TICSerializer(serializers.ModelSerializer):

    class Meta:
        model = TIC
        fields = ('id', 'title', 'icon', 'description', 'link')
