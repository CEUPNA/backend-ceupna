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

class TICViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = TIC.objects.all()
    serializer_class = TICSerializer
