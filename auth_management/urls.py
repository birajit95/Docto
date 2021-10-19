from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('new_access_token/', views.GetAccessTokenUsingRefreshToken.as_view()),
    path('change_password/', views.ChangePasswordAPIView.as_view()),
    path('forgot_password/', views.ForgotPasswordAPIView.as_view()),
    path('verify_password_reset_otp/', views.VerifyPasswordResetOTPAPIView.as_view()),
    path('reset_password/', views.ResetPasswordAPIView.as_view()),
    path('module_permissions/', views.ModulePermissionAPIView.as_view()),
    path('module_permissions/<int:pk>/', views.ModulePermissionRetrieveAPIView.as_view()),
    path('assign_modules/', views.ModuleGroupMapAPIView.as_view()),
    path('get_assigned_modules/<int:pk>/', views.GETGroupModulePermissionAPIView.as_view()),
    path('get_logs/', views.GetLogsAPIView.as_view())
]
