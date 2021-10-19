from rest_framework import serializers
from .models import User, DoctorDetails
from common.timezone_conversion import convert_tz
from common.age_calculator import calculate_age
from master_management.locations.serializers import AddressGetSerializer, AddressSerializer


class UserBaseSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'country_code', 'mobile', 'email', 'address']


class PatientGetSerializer(UserBaseSerializer):
    date_joined = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    address = AddressGetSerializer()

    class Meta(UserBaseSerializer.Meta):
        fields = ['id'] + UserBaseSerializer.Meta.fields + ['age', 'date_joined']

    def get_age(self, instance):
        if instance.dob:
            return calculate_age(instance.dob)

    def get_date_joined(self, instance):
        if instance.date_joined:
            return convert_tz(instance.date_joined)


class PatientRegistrationSerializer(UserBaseSerializer):
    confirm_password = serializers.CharField(min_length=6)
    address = AddressSerializer()

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + [
            'dob', 'password', 'confirm_password'
        ]
        extra_kwargs = {
            'dob': {'required': True}
        }

    def validate(self, data):
        email = data.get("email")
        mobile = data.get("mobile")
        password = data.get("password")
        confirm_password = data.get('confirm_password')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered")
        if mobile and User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("This mobile number is already registered")
        if password != confirm_password:
            raise serializers.ValidationError("password does not match, re-enter password")
        return data


class PatientProfile_1Serializer(UserBaseSerializer):
    address = AddressSerializer()

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields

    def validate(self, data):
        email = data.get("email")
        mobile = data.get("mobile")
        _id = self.instance.id
        if email and User.objects.exclude(id=_id).filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered")
        if mobile and User.objects.exclude(id=_id).filter(mobile=mobile).exists():
            raise serializers.ValidationError("This mobile number is already registered")
        return data


class DoctorGetSerializer(UserBaseSerializer):
    date_joined = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    address = AddressGetSerializer()

    class Meta(UserBaseSerializer.Meta):
        fields = ['id'] + UserBaseSerializer.Meta.fields + ['age', 'date_joined']

    def get_age(self, instance):
        if instance.dob:
            return calculate_age(instance.dob)

    def get_date_joined(self, instance):
        if instance.date_joined:
            return convert_tz(instance.date_joined)


class DoctorRegistrationSerializer(UserBaseSerializer):
    confirm_password = serializers.CharField(min_length=6)
    address = AddressSerializer()

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + [
            'dob', 'password', 'confirm_password'
        ]
        extra_kwargs = {
            'dob': {'required': True}
        }

    def validate(self, data):
        email = data.get("email")
        mobile = data.get("mobile")
        password = data.get("password")
        confirm_password = data.get('confirm_password')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered")
        if mobile and User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("This mobile number is already registered")
        if password != confirm_password:
            raise serializers.ValidationError("password does not match, re-enter password")
        return data


class DoctorProfile_1Serializer(UserBaseSerializer):
    address = AddressSerializer()

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields

    def validate(self, data):
        email = data.get("email")
        mobile = data.get("mobile")
        _id = self.instance.id
        if email and User.objects.exclude(id=_id).filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered")
        if mobile and User.objects.exclude(id=_id).filter(mobile=mobile).exists():
            raise serializers.ValidationError("This mobile number is already registered")
        return data


class UpdateDoctorProfile_2Serializer(serializers.ModelSerializer):
    qualifications = serializers.ListSerializer(
        child=serializers.DictField(required=True),
        help_text="""
            [
            {'course':'MBBS', 'institute_name':'AGMC', 'course_start_date': '2015-03-01', 'course_end_date':'2020-04-05'},
            {'course':'MD', 'institute_name':'AGMC', 'course_start_date': '2020-03-01', 'course_end_date':'2023-04-05'},
            {'course':'BHMS', 'institute_name':'AGMC', 'course_start_date': '2015-03-01', 'course_end_date':'2020-04-05'}
            ]
            """,
        required=True
    )

    class Meta:
        model = DoctorDetails
        fields = ["specialization", "qualifications", "practice_start_date", "registration_number"]

    def validate(self, data):
        qualifications = data.get("qualifications")
        registration_number = data.get("registration_number")
        qualification_keys = ['course', 'institute_name', 'course_start_date', 'course_end_date']
        # date_regex = "[1,2]{1}[0-9]{3}(-)[0-1]{1}[0-2]"

        if len(qualifications) == 0:
            raise serializers.ValidationError(f'At least one qualification information is required')

        for qualification in qualifications:
            if len(set(qualification.keys()).difference(set(qualification_keys))) > 0:
                raise serializers.ValidationError(f'Check qualification keys, fields are {qualification_keys}')
            if not qualification.get('course'):
                raise serializers.ValidationError(f'Course can not be blank')
            if not qualification.get('institute_name'):
                raise serializers.ValidationError(f'Course can not be blank')
            if not qualification.get('course_start_date'):
                raise serializers.ValidationError(f'course_start_date can not be blank')
            if not qualification.get('course_end_date'):
                raise serializers.ValidationError(f'course_end_date can not be blank')

            if not qualification.get('certificate_url'):
                qualification.update({
                    'certificate_url': None
                })
        if not registration_number:
            raise serializers.ValidationError("Registration number is required")
        if registration_number:
            # validate registration number
            pass
        return data


class QualificationSerializer(serializers.Serializer):
    course = serializers.CharField(max_length=300)
    institute_name = serializers.CharField(max_length=300)
    course_start_date = serializers.DateField()
    course_end_date = serializers.DateField()
    certificate_url = serializers.CharField(max_length=500)


class DoctorGetProfile_2Serializer(serializers.ModelSerializer):
    qualifications = QualificationSerializer(many=True)
    doctor = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()

    class Meta:
        model = DoctorDetails
        fields = ["doctor", "specialization", "qualifications", "practice_start_date", "registration_number",
                  "experience"]

    def get_doctor(self, instance):
        if instance.doctor:
            return {
                'doctor_id': instance.doctor.id,
                'doctor_name': instance.doctor.first_name + " " + instance.doctor.last_name
            }

    def get_experience(self, instance):
        if instance.practice_start_date:
            return calculate_age(instance.practice_start_date)


class UploadCertificateSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    course_number = serializers.IntegerField(required=True)

    def validate(self, data):
        file = data.get('file')
        course_number = data.get('course_number')

        allowed_file_extensions = ('.pdf', '.jpg', '.jpeg', 'png')

        if file:
            file_name = file._name
            if '.' + file_name.split('.')[1] not in allowed_file_extensions:
                raise serializers.ValidationError(f'only {allowed_file_extensions} extensions are allowed')
            file_size = file.size / (1024 * 1024)
            if file_size > 2:
                raise serializers.ValidationError(f'file size should not be greater than 2 MB')

        if course_number < 1 or course_number > 3:
            raise serializers.ValidationError('course number should be between 1 and 3')
        return data
