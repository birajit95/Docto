from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .models import DoctorTimings
from rest_framework.response import Response
from . import serializers as sr
from .models import Appointment, AppointmentPlan
from auth_management.auth_permission import BasicModelViewSet, permission_deco
from user_management.models import User, DoctorDetails
from master_management.locations.serializers import AddressGetSerializer
from common.time_format_conversion import _24hours_to_12hours
from common.get_day_and_time import get_day, get_time
from common.age_calculator import calculate_age
import random
import time


class AppointmentPlanAPIViewSet(BasicModelViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_name = 'APPOINTMENT-PLAN'

    queryset = AppointmentPlan.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return sr.AppointmentPlanCreateUpdateSerializer
        return sr.AppointmentPlanSerializer

    def perform_destroy(self, instance):
        instance.is_active = False


class DoctorTimingsAPIView(generics.GenericAPIView):
    serializer_class = sr.DoctorTimingsSerializer
    queryset = DoctorTimings.objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_name = 'DOCTOR_TIMINGS'

    @permission_deco(action='create')
    def post(self, request):
        """ This api is to create/update timings of doctor """
        data = request.data
        user = request.user
        try:
            serializer = sr.DoctorTimingsSerializer(data=data)
            if serializer.is_valid():
                timings = serializer.validated_data['timings']
                bulk_data = []
                DoctorTimings.objects.filter(doctor=user).delete()
                for time_data in timings:
                    day = time_data['day']
                    time_slot = time_data['time_slot']
                    for slot in time_slot:
                        start_time = slot['start_time']
                        end_time = slot['end_time']
                        bulk_data.append(DoctorTimings(doctor=user, day=day, start_time=start_time, end_time=end_time))
                DoctorTimings.objects.bulk_create(bulk_data)
                status_code = 200
                response = {'message': 'Timing dara saved'}
            else:
                status_code = 400
                response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
        except Exception as e:
            status_code = 500
            response = {'message': 'Internal server error'}
        return Response(response, status=status_code)

    @permission_deco(action='list')
    def get(self, request):
        """ This api is to fetch doctor timings """
        doctor_id = request.data.get('doctor_id')
        user = request.user
        execute_next_line = True
        if user.groups.filter(name__iexact='DOCTOR').exists():
            doctor = user
        else:
            try:
                doctor = User.objects.get(id=doctor_id, groups__name__in=['DOCTOR'])
            except User.DoesNotExist:
                execute_next_line = False
                response = {'message': 'Doctor not found with this id'}
                status_code = 404
        if execute_next_line:
            doc_timings = DoctorTimings.objects.filter(doctor=doctor)
            timings_list = []
            day_set = set()
            for timing in doc_timings:
                day_set.add(timing.day)
            for day in day_set:
                data_dict = {
                    'day': day,
                    'time_slot': []
                }
                for time_data in doc_timings:
                    if day == time_data.day:
                        data_dict['time_slot'].append({
                            'start_time': _24hours_to_12hours(str(time_data.start_time)),
                            'end_time': _24hours_to_12hours(str(time_data.end_time))
                        })
                timings_list.append(data_dict)
            response = {'timings': timings_list}
            status_code = 200

        return Response(response, status=status_code)


class SearchDoctorAPIView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_name = 'DOCTOR_SEARCH'

    def get_qualification_brief(self, qualifications):
        qualification_list = [
            {
                'course': qua['course'],
                'institute_name': qua['institute_name']
            }
            for qua in qualifications
        ]
        return qualification_list

    @permission_deco(action='list')
    def get(self, request):
        specialization = request.query_params.get('specialization')
        try:
            today = get_day()
            time = get_time()
            query = Q(is_busy=False, day=today, start_time__lte=time, end_time__gte=time)
            if specialization:
                query.add(Q(doctor__doctor_details__specialization__name__in=[specialization]), Q.AND)
            doc_timings = DoctorTimings.objects.filter(
                query
            )
            data_length = doc_timings.count()
            random_sample = random.sample(sorted(doc_timings, key=lambda x: x.doctor.id), min(data_length, 2))
            doctor_ids = [x.doctor.id for x in random_sample]
            doc_details = sorted(DoctorDetails.objects.filter(doctor__id__in=doctor_ids), key=lambda x: x.doctor.id)
            merge_data_list = []
            for i in range(len(random_sample)):
                doc_timing = random_sample[i]
                doc_detail = doc_details[i]
                data_dict = {
                    'doctor_id': doc_detail.doctor.id,
                    'doctor_name': doc_detail.doctor.get_full_name(),
                    'address': AddressGetSerializer(doc_detail.doctor.address).data,
                    'specialization': doc_detail.specialization.name,
                    'is_verified': doc_detail.is_verified,
                    'qualifications': self.get_qualification_brief(doc_detail.qualifications),
                    'experience': calculate_age(doc_detail.practice_start_date),
                    'start_time': _24hours_to_12hours(doc_timing.start_time),
                    'end_time': _24hours_to_12hours(doc_timing.end_time)
                }
                merge_data_list.append(data_dict)
            response = merge_data_list
            status_code = 200
        except Exception as e:
            response = {'message': 'Internal server error'}
            status_code = 500

        return Response(response, status=status_code)

#
# class SessionAPIView(APIView):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.module_name = 'LIVE-SESSION'
#
#     def get_session_id(self, doctor, patient):
#         return doctor.username + "_" + patient.username + str(time.time()).split('.')[0]
#
#     def post(self, request):
#         """ This is to start a session """
#         data = request.data
#         serializer = sr.SessionSerializer(data=data)
#         if serializer.is_valid():
#             doctor = serializer.validated_data['doctor']
#             patient = serializer.validated_data['patient']
#             session_id = self.get_session_id(doctor, patient)
#             Appointment.objects.create(session_id=session_id, doctor=doctor, patient=patient, )
#         else:
#             pass
