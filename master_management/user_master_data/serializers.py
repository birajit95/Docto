from rest_framework import serializers
from .models import Doctor_Type


class DoctorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor_Type
        fields = '__all__'

    def validate(self, data):

        name = data.get('name')
        if Doctor_Type.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError(
                'This Type is already present'
            )
        return data