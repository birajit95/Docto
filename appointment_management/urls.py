from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('appointment_plans', views.AppointmentPlanAPIViewSet, basename='appointment-plans')

urlpatterns = [
    path('', include(router.urls)),
    path('doctor_timings/', views.DoctorTimingsAPIView.as_view()),
    path('search_doctor/', views.SearchDoctorAPIView.as_view())
]
