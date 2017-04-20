# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Center, Teacher, TIC


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ('id', 'center_id', 'name', 'acronym', 'email', 'telephone', 'url')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'upna_id', 'name', 'email', 'telephone', 'timetable')


class TICSerializer(serializers.ModelSerializer):
    class Meta:
        model = TIC
        fields = ('id', 'name', 'icon', 'description', 'url')
