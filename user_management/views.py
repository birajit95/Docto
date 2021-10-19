from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
from rest_framework.response import Response
from . import serializers as sr
from .models import User, DoctorDetails
from django.contrib.auth.models import Group
from common.generate_username import get_username
from common.file_upload import upload_file
from master_management.locations.models import Address
from auth_management.auth_permission import BasicModelViewSet, permission_deco
from rest_framework.decorators import action


class PatientViewSet(BasicModelViewSet):
    queryset = User.objects.filter(
        is_active=True,
        groups__name__in=["PATIENT"]
    ).select_related(
        'address'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_name = "PATIENT"

    def get_serializer_class(self):
        if self.action == 'create':
            return sr.PatientRegistrationSerializer
        if self.action == 'update':
            return sr.PatientProfile_1Serializer
        return sr.PatientGetSerializer

    def create(self, request, *args, **kwargs):
        """"This api is used to register patient"""
        try:
            data = request.data
            serializer = self.get_serializer_class()(data=data)
            if serializer.is_valid():
                serializer.validated_data.pop('confirm_password')
                serializer.validated_data["username"] = get_username('patient')
                serializer.validated_data["password"] = make_password(serializer.validated_data["password"])
                address = serializer.validated_data.pop('address')
                address_instance = Address.objects.create(**address)
                serializer.validated_data['address'] = address_instance
                instance = serializer.save()
                group = Group.objects.filter(name__iexact='patient').first()
                instance.groups.add(group)
                serializer = sr.PatientGetSerializer(instance=instance)
                response = serializer.data
                status_code = status.HTTP_201_CREATED
            else:
                response = {"message": {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
                status_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {"message": "Internal Server Error"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status_code)

    @permission_deco(action='update')
    def update(self, request, *args, **kwargs):
        response = {"message": "This method is not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(methods=['GET', 'PUT'], detail=False)
    @permission_deco(action='profile_1')
    def patient_profile_1(self, request):
        user = request.user
        if user.groups.filter(name='PATIENT'):
            if request.method == 'PUT':
                data = request.data
                serializer = sr.PatientProfile_1Serializer(instance=user, data=data, partial=True)
                if serializer.is_valid():
                    if serializer.validated_data.get('address'):
                        address_data = serializer.validated_data.pop('address')
                        address_ser = sr.AddressSerializer(instance=user.address, data=address_data, partial=True)
                        address_ser.is_valid(raise_exception=True)
                        address_instance = address_ser.save()
                        serializer.validated_data['address'] = address_instance
                    instance = serializer.save(instance=user)
                    serializer = sr.PatientGetSerializer(instance=instance)
                    response = serializer.data
                    status_code = status.HTTP_200_OK
                else:
                    response = {"message": {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
                    status_code = status.HTTP_404_NOT_FOUND
            else:
                serializer = sr.PatientGetSerializer(user)
                response = serializer.data
                status_code = status.HTTP_200_OK
        else:
            response = {"message": 'Patient profile action not allowed'}
            status_code = status.HTTP_403_FORBIDDEN
        return Response(response, status=status_code)


class DoctorAPIViewSet(BasicModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_name = "DOCTOR"

    queryset = User.objects.filter(
        is_active=True,
        groups__name__in=["DOCTOR"]
    ).select_related(
        'address'
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return sr.DoctorRegistrationSerializer
        if self.action == 'update':
            return sr.DoctorProfile_1Serializer
        if self.name == 'profile_2':
            return sr.UpdateDoctorProfile_2Serializer
        return sr.DoctorGetSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @permission_deco(action='update')
    def update(self, request, *args, **kwargs):
        response = {"message": "This method is not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        """"This api is for doctor registrations"""
        try:
            data = request.data
            serializer = self.get_serializer_class()(data=data)
            if serializer.is_valid():
                serializer.validated_data.pop('confirm_password')
                serializer.validated_data["username"] = get_username('doctor')
                serializer.validated_data["password"] = make_password(serializer.validated_data["password"])
                address = serializer.validated_data.pop('address')
                address_instance = Address.objects.create(**address)
                serializer.validated_data['address'] = address_instance
                instance = serializer.save()
                group = Group.objects.filter(name__iexact='doctor').first()
                instance.groups.add(group)
                serializer = sr.DoctorGetSerializer(instance=instance)
                response = serializer.data
                status_code = status.HTTP_201_CREATED
            else:
                response = {"message": {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
                status_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {"message": "Internal Server Error"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status_code)

    @action(methods=['GET', 'PUT'], detail=False)
    @permission_deco(action='profile_1')
    def doctor_profile_1(self, request):
        user = request.user
        if user.groups.filter(name='DOCTOR'):
            if request.method == 'PUT':
                data = request.data
                serializer = sr.DoctorProfile_1Serializer(instance=user, data=data, partial=True)
                if serializer.is_valid():
                    if serializer.validated_data.get('address'):
                        address_data = serializer.validated_data.pop('address')
                        address_ser = sr.AddressSerializer(instance=user.address, data=address_data, partial=True)
                        address_ser.is_valid(raise_exception=True)
                        address_instance = address_ser.save()
                        serializer.validated_data['address'] = address_instance
                    instance = serializer.save(instance=user)
                    serializer = sr.DoctorGetSerializer(instance=instance)
                    response = serializer.data
                    status_code = status.HTTP_200_OK
                else:
                    response = {"message": {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
                    status_code = status.HTTP_404_NOT_FOUND
            else:
                serializer = sr.PatientGetSerializer(user)
                response = serializer.data
                status_code = status.HTTP_200_OK
        else:
            response = {"message": 'Doctor profile action not allowed'}
            status_code = status.HTTP_403_FORBIDDEN
        return Response(response, status=status_code)

    @action(methods=['GET', 'PUT'], detail=False, name='profile_2')
    @permission_deco(action='profile_2')
    def doctor_profile_2(self, request):
        user = request.user
        if request.method == "PUT":
            data = request.data
            data_exists = False
            if DoctorDetails.objects.filter(doctor=user).exists():
                data_exists = True
                serializer = sr.UpdateDoctorProfile_2Serializer(data=data, instance=user)
            else:
                serializer = sr.UpdateDoctorProfile_2Serializer(data=data)
            if serializer.is_valid():
                if not data_exists:
                    serializer.validated_data['doctor'] = user
                    serializer.save()
                else:
                    serializer.save(instance=user)
                status_code = status.HTTP_200_OK
                response = {'message': 'Data updated'}
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
        else:
            data = DoctorDetails.objects.filter(doctor=user).first()
            serializer = sr.DoctorGetProfile_2Serializer(data)
            response = serializer.data
            status_code = 200
        return Response(response, status=status_code)

    @action(methods=['POST'], detail=False, name='upload_certificate')
    @permission_deco(action='certificate_upload')
    def upload_certificate(self, request):
        user = request.user
        course_number = request.query_params.get('course_number')
        file = request.FILES.get('certificate')
        request_data = {
            'course_number': course_number,
            'file': file
        }
        try:
            serializer = sr.UploadCertificateSerializer(data=request_data)
            if serializer.is_valid():
                file = serializer.validated_data['file']
                course_number = serializer.validated_data['course_number']
                file_url = upload_file(file, subdir='certificates')
                doctor_details = DoctorDetails.objects.filter(doctor=user).first()
                qualifications = doctor_details.qualifications
                qualifications[course_number - 1].update(
                    {
                        'certificate_url': file_url
                    }
                )
                doctor_details.qualifications = qualifications
                doctor_details.save()
                status_code = 200
                response = {'message': 'Certificate uploaded successfully'}
            else:
                status_code = 400
                response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
        except Exception as e:
            status_code = 500
            response = {'message': 'Internal server error'}
        return Response(response, status=status_code)


