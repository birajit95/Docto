import jwt
from decouple import config
from datetime import datetime, timedelta
from user_management.models import User
from rest_framework import authentication


class JWTAuth:
    @staticmethod
    def getAccessToken(username, password):
        pay_load = {
            'username': username,
            'password': password,
            'grant_type': 'access_token',
            'exp': datetime.utcnow() + timedelta(days=int(config("ACCESS_TOKEN_EXP_TIME")))
        }
        jwt_token = jwt.encode(pay_load, key=config('SECRET_KEY'))
        return jwt_token

    @staticmethod
    def getRefreshToken(username, password):
        pay_load = {
            'username': username,
            'password': password,
            'grant_type': 'refresh_token',
            'exp': datetime.utcnow() + timedelta(days=int(config("REFRESH_TOKEN_EXP_TIME")))
        }
        jwt_token = jwt.encode(pay_load, key=config('SECRET_KEY'))
        return jwt_token

    @staticmethod
    def getResetToken(username, password):
        pay_load = {
            'username': username,
            'password': password,
            'grant_type': 'reset_token',
            'exp': datetime.utcnow() + timedelta(minutes=5)
        }
        jwt_token = jwt.encode(pay_load, key=config('SECRET_KEY'))
        return jwt_token

    @staticmethod
    def verifyToken(jwt_token):
        try:
            verification_status = jwt.decode(jwt_token, key=config('SECRET_KEY'), algorithms='HS256')
            return verification_status
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        except Exception:
            return False


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        headers = request.headers
        token = headers.get('Authorization')
        jwt_status = JWTAuth.verifyToken(token)
        user = None
        if jwt_status and jwt_status.get('grant_type') == 'access_token':
            username = jwt_status.get('username')
            try:
                user = User.objects.get(username=username)
            except Exception:
                user = None
        return user, None
