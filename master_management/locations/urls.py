from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('timezones', views.TimezoneViewSet, basename='timezones')
router.register('countries', views.CountryViewSet, basename='countries')
router.register('states', views.StateViewSet, basename='states')
router.register('cities', views.CityViewSet, basename='cities')
router.register('addresses', views.AddressViewSet, basename='addresses')


urlpatterns = [
    path('', include(router.urls))
]
