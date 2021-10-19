from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Timezone, City, State, Country, Address
from . import serializers as sr


class TimezoneViewSet(ModelViewSet):
    queryset = Timezone.objects.filter(is_active=True)
    serializer_class = sr.TimezoneSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.filter(is_active=True)
    serializer_class = sr.CountrySerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class StateViewSet(ModelViewSet):
    queryset = State.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return sr.StateGetSerializer
        return sr.StateSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CityViewSet(ModelViewSet):
    queryset = City.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return sr.CityGetSerializer
        return sr.CitySerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class AddressViewSet(ReadOnlyModelViewSet):
    queryset = Address.objects.filter(is_active=True)
    serializer_class = sr.AddressGetSerializer

