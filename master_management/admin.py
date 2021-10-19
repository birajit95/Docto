from django.contrib import admin
from .models import *

admin.site.register(Timezone)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Address)
admin.site.register(Doctor_Type)

