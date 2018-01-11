# -*- coding: utf-8 -*-

from rest_framework import serializers

from . import models


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
    representative_members = serializers.SerializerMethodField()
    quality_representative_members = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return NameSerializer(obj).data

    @staticmethod
    def get_representative_members(obj):
        num_rep = obj.number_representative_members
        q = models.CenterRepresentative.objects.filter(center=obj).order_by('-init_date')[:num_rep].values(
            'representative')
        qq = models.Representative.objects.filter(id__in=q)
        return RepresentativeSerializer(qq, many=True).data

    @staticmethod
    def get_quality_representative_members(obj):
        num_rep = obj.number_quality_representative_members
        q = models.CenterQualityRepresentative.objects.filter(center=obj).order_by('-init_date')[:num_rep].values(
            'representative')
        qq = models.Representative.objects.filter(id__in=q)
        return RepresentativeSerializer(qq, many=True).data

    class Meta:
        model = models.Center
        exclude = ('name_es', 'name_eus', 'name_en')


class DegreeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    center = CenterSerializer(many=True)

    @staticmethod
    def get_name(obj):
        return NameSerializer(obj).data

    class Meta:
        model = models.Degree
        depth = 1
        exclude = ('name_es', 'name_eus', 'name_en')


class DepartmentSerializer(serializers.ModelSerializer):
    representative_members = serializers.SerializerMethodField()

    @staticmethod
    def get_representative_members(obj):
        num_rep = obj.number_representative_members
        q = models.DepartmentRepresentative.objects.filter(department=obj).order_by('-init_date')[:num_rep].values('representative')
        qq = models.Representative.objects.filter(id__in=q)
        return RepresentativeSerializer(qq, many=True).data

    class Meta:
        model = models.Department
        depth = 1
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Representative
        fields = '__all__'


class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('id', 'name',)


class SubjectDetailSerializer(serializers.ModelSerializer):
    web = serializers.ReadOnlyField()  # Campos generados al vuelo.
    bibliography = serializers.ReadOnlyField()

    class Meta:
        model = models.Subject
        depth = 1
        fields = '__all__'


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('id', 'name',)


class TeacherDetailSerializer(serializers.ModelSerializer):
    web = serializers.ReadOnlyField()  # Campos generados al vuelo.

    #  subjects = serializers.ReadOnlyField()

    class Meta:
        model = models.Teacher
        fields = '__all__'


class TICListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TIC
        fields = ('id', 'name', 'icon')


class TICDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TIC
        fields = '__all__'
