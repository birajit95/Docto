from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('patients', views.PatientViewSet, basename='patients')
router.register('doctors', views.DoctorAPIViewSet, basename='doctors')

urlpatterns = [
    path('', include(router.urls)),
]
