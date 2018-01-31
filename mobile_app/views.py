# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response

from . import models
from . import serializers
from .management.bus_timetable import get_bus_timetables


class BusViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.BusSerializer
    queryset = list()

    def list(self, request):
        serializer = self.get_serializer(get_bus_timetables(), many=True)
        return Response(serializer.data)


class CenterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los Centros de la Universidad.
    """
    queryset = models.Center.objects.all()
    serializer_class = serializers.CenterSerializer


class DegreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las titulaciones de la Universidad.
    """
    queryset = models.Degree.objects.prefetch_related('center').all()
    serializer_class = serializers.DegreeSerializer

    def get_queryset(self):
        """
        Método para gestionar los filtros sobre las titulaciones. Puede pedirse:
            - Un subconjunto de las grado dado el id del centro.
        :return: Una subconjunto de las titulaciones con los criterios previstos.
        """
        queryset = models.Degree.objects.all()
        center_id = self.request.query_params.get('center_id', None)
        if center_id is not None:
            queryset = queryset.filter(degree__center__center_id__exact=center_id).distinct()
        return queryset


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los departamentos de la UPNA.
    """
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.filter(active=True)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las actividades de la UPNA.
    """
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()


class CEUPNAEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las actividades de la UPNA.
    """
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all().filter(schedule__exact='ceupna')


class InstEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las actividades de la UPNA.
    """
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all().filter(schedule__exact='inst')


class RepresentativeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los representantes de la Universidad
    """
    serializer_class = serializers.ShortRepresentativeSerializer
    queryset = models.Representative.objects.all()


class RuleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los representantes de la Universidad
    """
    resource_name = 'rule-version'
    serializer_class = serializers.RuleSerializer
    queryset = models.Rule.objects.all()


class RuleVersionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los representantes de la Universidad
    """
    serializer_class = serializers.RuleVersionSerializer
    queryset = models.RuleVersion.objects.all()

class UniqueRepreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.UniqueResponsibilitySerializer
    queryset = models.Responsibility.objects.all()


class StudentCouncilViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.StudentCouncilSerializer
    queryset = models.StudentCouncil.objects.all()


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las asignaturas de las titulaciones de la Universidad.
    """

    def get_queryset(self):
        """
        Método para gestionar los filtros sobre las asignaturas. Puede pedirse:
            - Un subconjunto de las asignaturas dado el id que  utiliza la UPNA.
            - Un subconjunto de las asignaturas dado el id del grado en la base de datos.
            - Un subconjunto de las asignatruas dado el id del grado que utiliza la UPNA.
        :return: Una subconjunto de las asignaturas con los criterios previstos.
        """
        queryset = models.Subject.objects.all()
        upna_id = self.request.query_params.get('upna_id', None)
        degree_id = self.request.query_params.get('degree_id', None)
        upna_degree_id = self.request.query_params.get('upna_degree_id', None)
        if upna_id is not None:
            queryset = queryset.filter(upna_id__exact=upna_id)
        if degree_id is not None:
            queryset = queryset.filter(degree_id__exact=degree_id).distinct()
        if upna_degree_id is not None:
            queryset = queryset.filter(degree__upna_id__exact=upna_degree_id)

        return queryset

    def get_serializer_class(self):
        """
        Método para permitir disponer de los argumentos adecuados en la vista de lista y de detalle.
        :return: El serializador correcto según el tipo de petición.
        """
        if self.action == 'list':
            return serializers.SubjectListSerializer
        else:
            return serializers.SubjectDetailSerializer


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los profesores de la Universidad
    """

    def get_queryset(self):
        """
        Método para gestionar los filtros sobre las asignaturas. Puede pedirse:
            - Un subconjunto de los profesores dado un string que coincide total o parcialmente con su nombre.
            - Un subconjunto de los profesores dado el identificador que se les concede en la UPNA.
            - Un subconjunto de las asignaturas dado el id del grado que utiliza la base de datos.
            - Un subconjunto de las asignaturas dado el id del grado que utiliza la UPNA.
        :return: Una subconjunto de los profesores con los criterios previstos.
        """
        queryset = models.Teacher.objects.all()
        name = self.request.query_params.get('name', None)
        upna_id = self.request.query_params.get('upna_id', None)
        degree_id = self.request.query_params.get('degree_id', None)
        upna_degree_id = self.request.query_params.get('upna_degree_id', None)
        subject_id = self.request.query_params.get('subject_id', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if upna_id is not None:
            queryset = queryset.filter(upna_id__exact=upna_id)
        if degree_id is not None:
            queryset = queryset.filter(subject__degree__id__exact=degree_id).distinct()
        if upna_degree_id is not None:
            queryset = queryset.filter(subject__degree__upna_id__exact=degree_id).distinct()
        if subject_id is not None:
            queryset = queryset.filter(subject__id=subject_id)
        return queryset

    def get_serializer_class(self):
        """
        Método para permitir disponer de los argumentos adecuados en la vista de lista y de detalle.
        :return: El serializador correcto según el tipo de petición.
        """
        if self.action == 'list' and self.request.query_params.get('subject_id', None) is None:
            return serializers.TeacherListSerializer
        else:
            return serializers.TeacherDetailSerializer


class TICViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los recursos TIC de la Universidad.
    """
    queryset = models.TIC.objects.all()

    def get_serializer_class(self):
        """
        Método para permitir disponer de los argumentos adecuados en la vista de lista y de detalle.
        :return: El serializador correcto según el tipo de petición.
        """
        if self.action == 'list':
            return serializers.TICListSerializer
        else:
            return serializers.TICDetailSerializer


# Web
# https://chastityslave2556.tumblr.com/
# https://chirenon.tumblr.com/post/149470265042/seth-finds-out-that-he-and-brad-wont-be-switching
# https://chirenon.tumblr.com/archive
# http://obeyedyoungster.tumblr.com
# http://briefsboy22.tumblr.com/page/45
# http://maleinchastitycage.tumblr.com/
# https://chirenon.tumblr.com/post/168827792862
# http://obeyedyoungster.tumblr.com/post/168056977234/follow-me-obeyedyoungster
# http://ruinedorgasms.tumblr.com/post/167609054627
# http://obeyedyoungster.tumblr.com/post/168056977234/follow-me-obeyedyoungster
# https://hornytwinkcock.tumblr.com/
# http://chastity93.tumblr.com/page/22
# https://embarrassedboys.tumblr.com/post/68555312651
# https://domtopsir.tumblr.com/post/169076384506
# https://chastitypupboy.tumblr.com
# https://tightlypacked.tumblr.com
# https://hornywaterpologuy.tumblr.com/
# https://straightslaves.tumblr.com
# https://ottawasub.tumblr.com/
# https://mastersebparis.tumblr.com/
# http://hardmaster999.tumblr.com/
# https://dumb-horny-superhero.tumblr.com
# https://username108926.tumblr.com/
# https://cademicante.tumblr.com/post/165682727284
# http://ropedboys.tumblr.com/
# https://trainer48.tumblr.com/
