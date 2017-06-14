# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Center, Degree, Subject, Teacher, TIC


class CenterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ('name_es', 'name_eus', 'name_en')


class CenterSerializer(serializers.ModelSerializer):
    # name = CenterNameSerializer()
    class Meta:
        model = Center
        fields = '__all__'
        # fields = ('name', 'web', 'email')


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        depth = 1
        fields = '__all__'
#        exclude = ('created',)


class SubjectSerializer(serializers.ModelSerializer):
    web = serializers.ReadOnlyField()  # Campos generados al vuelo.
    bibliography = serializers.ReadOnlyField()

    class Meta:
        model = Subject
        depth = 1
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    web = serializers.ReadOnlyField()  # Campos generados al vuelo.

    class Meta:
        model = Teacher
        fields = '__all__'


class TICSerializer(serializers.ModelSerializer):
    class Meta:
        model = TIC
        fields = '__all__'
