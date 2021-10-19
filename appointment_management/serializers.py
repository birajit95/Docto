from rest_framework import serializers
from common.time_format_conversion import _12hours_to_24hours
from .models import DoctorTimings, AppointmentPlan, Appointment
from user_management.models import User


class TimeSlotSerializer(serializers.Serializer):
    start_time = serializers.CharField(required=True)
    end_time = serializers.CharField(required=True)


class TimingsSerializer(serializers.ModelSerializer):
    time_slot = serializers.ListField(
        child=TimeSlotSerializer()
    )

    class Meta:
        model = DoctorTimings
        fields = ['day', 'time_slot']


class DoctorTimingsSerializer(serializers.Serializer):
    timings = serializers.ListField(
        child=TimingsSerializer(),
        required=True
    )

    def validate(self, data):
        timings = data.get('timings')

        timing_day_keys = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]

        for time_data in timings:
            day = time_data['day']
            if day not in timing_day_keys:
                raise serializers.ValidationError(f"Please choose proper day, options are {timing_day_keys}")
            time_slots = time_data['time_slot']
            for slot in time_slots:
                start_time = slot["start_time"]
                end_time = slot["end_time"]
                if not start_time or not end_time:
                    raise serializers.ValidationError(f"start time or end time can not be blanked")

                new_start, new_end = _12hours_to_24hours(start_time), _12hours_to_24hours(end_time)
                slot.update({
                    'start_time': new_start,
                    'end_time': new_end
                })
        return data


class AppointmentPlanCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentPlan
        fields = ['name', 'valid_days', 'price', 'actual_price']

    def get_discount(self, price, actual_price):
        discount = price - actual_price
        discount_percent = round((discount / price) * 100, 2)
        return discount, discount_percent

    def validate(self, data):
        price = data.get('price')
        actual_price = data.get('actual_price')

        if price < actual_price:
            raise serializers.ValidationError('actual price should not be greater than price')
        data['discount'], data['discount_percent'] = self.get_discount(price, actual_price)
        return data


class AppointmentPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentPlan
        fields = ['id', 'name', 'valid_days', 'price', 'actual_price', 'discount', 'discount_percent']


# class Appointment(serializers.Serializer):
#     doctor = serializers.IntegerField()
#     patient = serializers.IntegerField()
#
#     def validate(self, data):
#         doctor_id = data.get('doctor')
#         patient_id = data.get('patient')
#         doctor = User.objects.filter(id=doctor_id, groups__name__iexact='Doctor').first()
#         patient = User.objects.filter(id=patient_id, groups__name__iexact='Patient').first()
#         if not doctor:
#             raise serializers.ValidationError("Doctor not found with this id")
#         if not patient:
#             raise serializers.ValidationError("Patient not found with this id")
#         data.update({
#             'doctor': doctor,
#             'patient': patient
#         })
#         return data
