# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Center, Degree, Subject, Teacher, TIC


class NameSerializer(serializers.Serializer):
    es = serializers.CharField(source='name_es')
    eus = serializers.CharField(source='name_eus')
    en = serializers.CharField(source='name_en')

    class Meta:
        fields = ('es', 'eus', 'en')


class CenterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return NameSerializer(obj).data

    class Meta:
        model = Center
        exclude = ('name_es', 'name_eus', 'name_en')

class DegreeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    center = CenterSerializer(many=True)

    def get_name(self, obj):
        return NameSerializer(obj).data

    class Meta:
        model = Degree
        depth = 1
        exclude = ('name_es', 'name_eus', 'name_en')



class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name',)


class SubjectDetailSerializer(serializers.ModelSerializer):
    web = serializers.ReadOnlyField()  # Campos generados al vuelo.
    bibliography = serializers.ReadOnlyField()

    class Meta:
        model = Subject
        depth = 1
        fields = '__all__'


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name',)


class TeacherDetailSerializer(serializers.ModelSerializer):
    web = serializers.ReadOnlyField()  # Campos generados al vuelo.

    class Meta:
        model = Teacher
        fields = '__all__'


class TICListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TIC
        fields = ('id', 'name', 'icon')


class TICDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TIC
        fields = '__all__'
