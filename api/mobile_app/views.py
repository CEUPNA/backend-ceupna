# -*- coding: utf-8 -*-

from .models import Center, Degree, Subject, Teacher, TIC
from .serializers import CenterSerializer, DegreeSerializer, SubjectSerializer, TeacherSerializer, TICSerializer
from rest_framework import viewsets


class CenterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los Centros de la Universidad.
    """
    queryset = Center.objects.all()
    serializer_class = CenterSerializer


class DegreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las titulaciones de la Universidad.
    """
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer

    #TODO: HAcer algo para ver los grados dado el código de un cierto centro.


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las asignaturas de las titulaciones de la Universidad.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    #TODO: HAcer algo para ver las asignaturas dado el código de un cierto grado.


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los profesores de la Universidad
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        """
        Método para gestionar la búsqueda de profesores por nombre.
        Es case insensitive y se encarga de buscar la selección como substrings.
        :return: Una selección de todos los profesores que cumplen el criterio del nombre.
        """
        queryset = Teacher.objects.all()
        name = self.request.query_params.get('name', None)
        upna_id = self.request.query_params.get('upna_id', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        elif upna_id is not None:
            queryset = queryset.filter(upna_id__exact=upna_id)
        return queryset


class TICViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los recursos TIC de la Universidad.
    """
    queryset = TIC.objects.all()
    serializer_class = TICSerializer
