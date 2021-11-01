import json
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from . import serializers as sr
from user_management.models import User
from common.opt_generation import generate_otp
from .models import OTPModel, Permission
from django.core.exceptions import ObjectDoesNotExist
from .jwt import JWTAuth
from .auth_permission import superuser_dec, auth_dec
import logging
import traceback
from datetime import datetime, timedelta
from DOCTO.settings import BASE_DIR
from django.contrib.auth.models import Group
import os


class LoginAPIView(generics.GenericAPIView):
    serializer_class = sr.LoginSerializer

    def post(self, request):
        data = request.data
        serializer = sr.LoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            filter_query = Q(mobile=username)
            filter_query.add(Q(email=username), Q.OR)
            try:
                user = User.objects.get(filter_query)
                is_valid = user.check_password(raw_password=password)
                if is_valid:
                    access_token = JWTAuth.getAccessToken(user.username, user.password)
                    refresh_token = JWTAuth.getRefreshToken(user.username, user.password)
                    response = {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'name': user.first_name + user.last_name,
                        'is_superuser': user.is_superuser
                    }
                    status_code = status.HTTP_200_OK
                else:
                    status_code = status.HTTP_401_UNAUTHORIZED
                    response = {'message': 'username or password deos not match!'}
            except ObjectDoesNotExist as e:
                status_code = status.HTTP_401_UNAUTHORIZED
                response = {'message': 'username or password deos not match!'}
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
        return Response(response, status=status_code)


class GetAccessTokenUsingRefreshToken(APIView):
    def post(self, request):
        jwt_token = request.headers.get('Authorization')
        jwt_data = JWTAuth.verifyToken(jwt_token=jwt_token)
        if jwt_data and jwt_data.get('grant_type') == 'refresh_token':
            username = jwt_data.get('username')
            password = jwt_data.get('password')
            access_token = JWTAuth.getAccessToken(username, password)
            refresh_token = JWTAuth.getRefreshToken(username, password)
            response = {
                "new_access_token": access_token,
                "new_refresh_token": refresh_token
            }
            status_code = status.HTTP_200_OK
        else:
            response = {
                'message': 'Your refresh token is either invalid or expired'
            }
            log1 = logging.getLogger('log1')
            log1.error('Your refresh token is either invalid or expired')
            status_code = status.HTTP_401_UNAUTHORIZED
        return Response(response, status=status_code)


class ChangePasswordAPIView(APIView):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.module_name = 'change_password'

    @auth_dec()
    def post(self, request):
        try:
            data = request.data
            user = request.user
            serializer = sr.ChangePasswordSerializer(instance=user, data=data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get('new_password')
                user.set_password(new_password)
                user.save()
                response = {'message': 'Your password is changed successfully'}
                status_code = status.HTTP_200_OK
            else:
                response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
                status_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(traceback.format_exc())
            response = {'message': 'Internal server error'}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status_code)


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = sr.ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            mobile = serializer.validated_data.get('mobile')
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                OTPModel.objects.create(user=user, otp=otp)
                # send mail code
                response = {'message': 'Password reset OTP has been sent to your mail'}
                status_code = status.HTTP_200_OK
            except ObjectDoesNotExist:
                try:
                    user = User.objects.get(mobile=mobile)
                    otp = generate_otp()
                    OTPModel.objects.create(user=user, otp=otp)
                    # send sms code
                    response = {'message': 'Password reset OTP has been sent to your mobile'}
                    status_code = status.HTTP_200_OK
                except ObjectDoesNotExist:
                    response = {'message': 'User not found with this mail or mobile number'}
                    status_code = status.HTTP_404_NOT_FOUND
            except Exception as e:
                response = {'message': 'Internal server error'}
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)


class VerifyPasswordResetOTPAPIView(APIView):
    def post(self, request):
        mobile_or_email = request.data.get('mobile_or_email')
        otp = request.data.get('otp')
        try:
            query_filter = Q(mobile=mobile_or_email)
            query_filter.add(Q(email=mobile_or_email), Q.OR)
            user = User.objects.get(query_filter)
            stored_otp_obj = OTPModel.objects.filter(user=user).last()
            time_diff = datetime.now().replace(tzinfo=None) - stored_otp_obj.time.replace(tzinfo=None)
            if time_diff > timedelta(minutes=2):
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {'message': 'OTP Expired'}
            elif stored_otp_obj.otp == otp and not stored_otp_obj.is_verified:
                stored_otp_obj.is_verified = True
                stored_otp_obj.save()
                reset_token = JWTAuth.getResetToken(user.username, user.password)
                reset_password_url = '/api/auth/reset_password/' + '?reset_token=' + reset_token
                status_code = status.HTTP_200_OK
                response = {'message': 'OTP verified successfully', 'password_reset_url': reset_password_url}
            else:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {'message': 'OTP does not match'}
        except ObjectDoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {'message': 'user not found'}

        return Response(response, status=status_code)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        reset_token = request.query_params.get('reset_token')
        data = request.data
        serializer = sr.ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            reset_token_data = JWTAuth.verifyToken(reset_token)
            if reset_token_data and reset_token_data.get('grant_type') == 'reset_token':
                is_token_used = OTPModel.objects.filter(reset_token=reset_token).exists()
                if is_token_used:
                    response = {'message': 'This link is already used'}
                    status_code = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    username = reset_token_data.get('username')
                    new_password = serializer.validated_data.get('new_password')
                    try:
                        user = User.objects.get(username=username)
                        user.set_password(new_password)
                        user.save()
                        otp_obj = OTPModel.objects.filter(user=user).last()
                        if otp_obj:
                            otp_obj.reset_token = reset_token
                            otp_obj.save()
                        response = {'message': 'Password reset successfully'}
                        status_code = status.HTTP_200_OK
                    except ObjectDoesNotExist:
                        response = {'message': 'Invalid link found'}
                        status_code = status.HTTP_406_NOT_ACCEPTABLE
            else:
                response = {'message': 'Invalid link found'}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        else:
            response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)


class ModulePermissionAPIView(APIView):

    def get_queryset(self):
        groups = self.request.user.groups.all()
        return Permission.objects.filter(role__in=groups)

    @auth_dec()
    def get(self, request):
        response = []
        groups = self.request.user.groups.all()
        for group in groups:
            permissions = Permission.objects.filter(role=group)
            serializer = sr.ModulePermissionSerializer(permissions, many=True)
            data = {
                'role_id': group.id,
                'role': group.name,
                'modules': serializer.data
            }
            response.append(data)
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class ModulePermissionRetrieveAPIView(APIView):

    @auth_dec()
    def get(self, request, pk):
        response = []
        groups = self.request.user.groups.all()
        for group in groups:
            permissions = Permission.objects.filter(role=group, module__id=pk).first()
            serializer = sr.ModulePermissionSerializer(permissions)
            data = {
                'role_id': group.id,
                'role': group.name,
                'modules': serializer.data
            }
            response.append(data)
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class ModuleGroupMapAPIView(generics.GenericAPIView):
    serializer_class = sr.ModuleGroupMapSerializer

    @superuser_dec()
    def post(self, request):
        data = request.data
        serializer = sr.ModuleGroupMapSerializer(data=data)
        try:
            if serializer.is_valid():
                role = serializer.validated_data.get('role_id')
                modules = serializer.validated_data.get('modules')
                role_module_list = []
                Permission.objects.filter(role=role).delete()
                for module in modules:
                    perm_obj = Permission(role=role, module=module['module'], allowed_permissions=module['permissions'])
                    role_module_list.append(perm_obj)
                Permission.objects.bulk_create(role_module_list)
                status_code = status.HTTP_200_OK
                response = {'message': "Role permissions is updated"}
            else:
                response = {'message': {'error_keys': serializer.errors.keys(), 'error': serializer.errors}}
                status_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            response = {'message': "Internal Server error"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status_code)


class GETGroupModulePermissionAPIView(generics.GenericAPIView):

    def get_queryset(self):
        groups = self.request.user.groups.all()
        return Permission.objects.filter(role__in=groups)

    @superuser_dec()
    def get(self, request, pk):
        try:
            group = Group.objects.get(id=pk)

            permissions = Permission.objects.filter(role=group)
            serializer = sr.ModulePermissionSerializer(permissions, many=True)
            response = {
                'role_id': group.id,
                'role': group.name,
                'modules': serializer.data
            }
            status_code = status.HTTP_200_OK
        except ObjectDoesNotExist:
            response = {'message': f'Role with id {pk} not found'}
            status_code = status.HTTP_404_NOT_FOUND

        return Response(response, status=status_code)


class GetLogsAPIView(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        path = os.path.join(BASE_DIR, 'logs', "log1.log")
        f = open(path)
        lines = f.read().split("\n")
        data_list = []
        keys = ['log_level', 'created_at', 'message', 'file_path', 'method', 'line_no']
        for line in lines:
            content = line.split(' / ')
            data_list.append(
                dict(zip(keys, content))
            )
        return Response(data_list)

