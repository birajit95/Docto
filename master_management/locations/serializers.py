from rest_framework import serializers
from .models import Timezone, City, State, Country, Address


class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timezone
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'is_active': {'read_only': True}
        }


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'is_active': {'read_only': True}
        }


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['name', 'time_zone', 'country']


class StateGetSerializer(StateSerializer):
    time_zone = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta(StateSerializer.Meta):
        fields = ['id'] + StateSerializer.Meta.fields + ['is_active']

    def get_time_zone(self, instance):
        if instance.time_zone:
            return {
                'id': instance.time_zone.id,
                'name': instance.time_zone.name
            }

    def get_country(self, instance):
        if instance.country:
            return {
                'id': instance.country.id,
                'name': instance.country.name
            }


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'country', 'state']


class CityGetSerializer(CitySerializer):
    state = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta(CitySerializer.Meta):
        fields = ['id'] + CitySerializer.Meta.fields + ['is_active']

    def get_state(self, instance):
        if instance.state:
            return {
                'id': instance.state.id,
                'name': instance.state.name,
                'time_zone': instance.state.time_zone.name if instance.state.time_zone else None,
            }

    def get_country(self, instance):
        if instance.country:
            return {
                'id': instance.country.id,
                'name': instance.country.name
            }


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['id', 'is_active']


class AddressGetSerializer(AddressSerializer):
    city = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta(AddressSerializer.Meta):
        exclude = []

    def get_city(self, instance):
        if instance.country:
            return {
                'id': instance.city.id,
                'name': instance.city.name
            }

    def get_state(self, instance):
        if instance.state:
            return {
                'id': instance.state.id,
                'name': instance.state.name,
                'time_zone': instance.state.time_zone.name if instance.state.time_zone else None,
            }

    def get_country(self, instance):
        if instance.country:
            return {
                'id': instance.country.id,
                'name': instance.country.name
            }
