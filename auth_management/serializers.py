from rest_framework import serializers
from .models import Permission
from django.contrib.auth.models import Group
from .models import Module



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        old_password = data.get('old_password')
        user = self.instance
        if new_password != confirm_password:
            raise serializers.ValidationError('Password does not match')
        is_valid = user.check_password(raw_password=old_password)
        if not is_valid:
            raise serializers.ValidationError('Please check the old password')
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    mobile = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)

    def validate(self, data):
        email = data.get('email')
        mobile = data.get('mobile')

        if email is None and mobile is None:
            raise serializers.ValidationError(
                'email and mobile both field can not be blank together, pass either of one')
        if email and mobile:
            raise serializers.ValidationError(
                'email and mobile both field can not be passed together, pass either of one')
        return data


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError('Password does not match')
        return data


class ModulePermissionSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ['module']

    def get_module(self, instance):
        if instance.module:
            return {
                'module_id': instance.module.id,
                'module_name': instance.module.name,
                'allowed_permissions': instance.allowed_permissions
            }


class ModuleGroupMapSerializer(serializers.Serializer):
    role_id = serializers.IntegerField(required=True)
    modules = serializers.ListField(
        child=serializers.DictField(
            required=True
            ),
        required=True,
        help_text= """
        "modules": [
        {
          "module_id": 1,
          "permissions": ["create", "update", "list"]
        },
       {
          "module_id": 2,
          "permissions": ["create", "update", "list"]
        }
        ]     
        """
    )

    def validate(self, data):
        role_id = data.get("role_id")
        modules = data.get("modules")
        role = Group.objects.filter(id=role_id).first()
        if not role:
            raise serializers.ValidationError("No role found with this role_id")

        data['role_id'] = role

        modules_data_list = []
        for module in modules:
            if set(module.keys()).difference({"module_id", "permissions"}):
                raise serializers.ValidationError(f"module keys are not proper [ex: 'module_id', 'permissions'] at {module}")

            if type(module['permissions']) is not list or type(module['module_id']) is not int:
                raise serializers.ValidationError(f"module keys are not in proper type [ex: module_id: int, "
                                                  f"permissions: list] at {module}")

            module_obj = Module.objects.filter(id=module.get('module_id')).first()
            if not module_obj:
                raise serializers.ValidationError(f"module not found with this module id at {module}")

            modules_data_list.append(
                {
                    'module': module_obj,
                    'permissions': module['permissions']
                }
            )
        data['modules'] = modules_data_list
        return data

