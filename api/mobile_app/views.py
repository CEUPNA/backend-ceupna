# -*- coding: utf-8 -*-

from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework import viewsets


class TeacherViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
