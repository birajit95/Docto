from django.urls import path, include

urlpatterns = [
    path('locations/', include('master_management.locations.urls')),
    path('user_master_data/', include('master_management.user_master_data.urls'))
]
