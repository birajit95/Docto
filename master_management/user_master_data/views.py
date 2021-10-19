from auth_management.auth_permission import BasicModelViewSet
from . import serializers as sr
from .models import Doctor_Type


class DoctorTypeAPIViewSet(BasicModelViewSet):
    serializer_class = sr.DoctorTypeSerializer
    queryset = Doctor_Type.objects.filter(is_active=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_name = "DOCTOR-TYPE"

    def perform_delete(self, instance):
        instance.is_active = False
        instance.save()

