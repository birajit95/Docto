from django.http import JsonResponse
from functools import wraps
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import generics
from .models import Permission


def has_permissions(user, module_name, action):
    roles = user.groups.all()
    permission_obj = Permission.objects.filter(
        role__in=roles, module__name=module_name
    ).first()
    if permission_obj and action in permission_obj.allowed_permissions:
        return True
    return False


def permission_deco(action):
    def wrap(api):
        @wraps(api)
        def wrapped_f(*args, **kwargs):
            module_name = getattr(args[0], 'module_name')
            request = getattr(args[0], 'request')
            user = request.user
            if user:
                if has_permissions(user, module_name, action):
                    return api(*args, **kwargs)
                else:
                    return JsonResponse({"message": "You don't have permission for this action"}, status=403)
            else:
                return JsonResponse({"message": "You are not authorized"}, status=401)

        return wrapped_f

    return wrap


def superuser_dec():
    def wrap(api):
        @wraps(api)
        def wrapped_f(*args, **kwargs):
            request = getattr(args[0], 'request')
            user = request.user
            if user and user.is_superuser:
                return api(*args, **kwargs)
            else:
                return JsonResponse({"message": "You are not authorized, This is only for superuser"}, status=403)
        return wrapped_f
    return wrap


def auth_dec():
    def wrap(api):
        @wraps(api)
        def wrapped_f(*args, **kwargs):
            request = getattr(args[0], 'request')
            user = request.user
            if user:
                return api(*args, **kwargs)
            else:
                return JsonResponse({"message": "You are not authenticated"}, status=401)
        return wrapped_f
    return wrap


class BasicModelViewSet(ModelViewSet):

    @permission_deco(action='list')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_deco(action='destroy')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @permission_deco(action='create')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_deco(action='retrieve')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @permission_deco(action='update')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_deco(action='update')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class BasicListCreateAPIView(generics.ListCreateAPIView):
    @permission_deco(action='list')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_deco(action='create')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class BasicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    @permission_deco(action='destroy')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @permission_deco(action='retrieve')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @permission_deco(action='update')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_deco(action='update')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
