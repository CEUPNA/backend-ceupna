# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import (TIC, Center, Degree, Department, Event, Representative, Subject,
                     Teacher)


class BusTimetableSerializer(serializers.Serializer):
    line = serializers.CharField()
    time1 = serializers.CharField(required=False)
    time2 = serializers.CharField(required=False)
    direction = serializers.CharField(required=False)
    icon = serializers.CharField(required=False)
    extra = serializers.CharField(required=False)

    class Meta:
        fields = 'line', 'time1', 'time2', 'direction', 'icon', 'extra'


class BusSerializer(serializers.Serializer):
    stop_id = serializers.IntegerField()
    stop_name = serializers.CharField()
    stop_campus = serializers.CharField()
    timetables = serializers.ListSerializer(child=BusTimetableSerializer())

    def get_timetables(self, obj):
        print(obj)
        return BusTimetableSerializer(obj).data

    class Meta:
        fields = 'stop_id', 'stop_name', 'stop_campus', 'timetables'


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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        depth = 1
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = '__all__'


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

    #  subjects = serializers.ReadOnlyField()

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
