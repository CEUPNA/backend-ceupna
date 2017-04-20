# -*- coding: utf-8 -*-

from .models import Center, Teacher, TIC
from .serializers import CenterSerializer, TeacherSerializer, TICSerializer
from rest_framework import viewsets


class CenterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los Centros de la Universidad.
    """
    queryset = Center.objects.all()
    serializer_class = CenterSerializer


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
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TICViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los recursos TIC de la Universidad.
    """
    queryset = TIC.objects.all()
    serializer_class = TICSerializer
