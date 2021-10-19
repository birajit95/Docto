from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('doctor_types', views.DoctorTypeAPIViewSet, basename='doctor_types')


urlpatterns = [
    path('', include(router.urls))
]
