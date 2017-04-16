# -*- coding: utf-8 -*-

from .models import Teacher, TIC
from .serializers import TeacherSerializer, TICSerializer
from rest_framework import viewsets


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
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
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = TIC.objects.all()
    serializer_class = TICSerializer
