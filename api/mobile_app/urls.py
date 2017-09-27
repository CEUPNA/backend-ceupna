# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'centers', views.CenterViewSet)
router.register(r'degrees', views.DegreeViewSet)
router.register(r'subjects', views.SubjectViewSet, base_name='subjects')
router.register(r'teachers', views.TeacherViewSet, base_name='teachers')
router.register(r'tics', views.TICViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls))  # ,
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')) # Para la autentificacion
]
