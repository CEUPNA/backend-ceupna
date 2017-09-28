# -*- coding: utf-8 -*-

from .models import Center, Degree, Subject, Teacher, TIC
from .serializers import CenterSerializer, DegreeSerializer, SubjectDetailSerializer, \
    SubjectListSerializer, TeacherDetailSerializer, TeacherListSerializer, TICDetailSerializer, TICListSerializer
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
    queryset = Degree.objects.prefetch_related('center').all()
    serializer_class = DegreeSerializer

    def get_queryset(self):
        """
        Método para gestionar los filtros sobre las titulaciones. Puede pedirse:
            - Un subconjunto de las grado dado el id del centro.
        :return: Una subconjunto de las titulaciones con los criterios previstos.
        """
        queryset = Degree.objects.all()
        center_id = self.request.query_params.get('center_id', None)
        if center_id is not None:
            queryset = queryset.filter(degree__center__center_id__exact=center_id).distinct()
        return queryset


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de las asignaturas de las titulaciones de la Universidad.
    """
    #queryset = Subject.objects.all()
#    serializer_class = SubjectSerializer

    def get_queryset(self):
        """
        Método para gestionar los filtros sobre las asignaturas. Puede pedirse:
            - Un subconjunto de las asignaturas dado el id que  utiliza la UPNA.
            - Un subconjunto de las asignaturas dado el id del grado en la base de datos.
            - Un subconjunto de las asignatruas dado el id del grado que utiliza la UPNA.
        :return: Una subconjunto de las asignaturas con los criterios previstos.
        """
        queryset = Subject.objects.all()
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
            return SubjectListSerializer
        else:
            return SubjectDetailSerializer


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
        queryset = Teacher.objects.all()
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
            return TeacherListSerializer
        else:
            return TeacherDetailSerializer


class TICViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado y vista en detalle de los recursos TIC de la Universidad.
    """
    queryset = TIC.objects.all()

    def get_serializer_class(self):
        """
        Método para permitir disponer de los argumentos adecuados en la vista de lista y de detalle.
        :return: El serializador correcto según el tipo de petición.
        """
        if self.action == 'list':
            return TICListSerializer
        else:
            return TICDetailSerializer
#    serializer_class = TICSerializer
