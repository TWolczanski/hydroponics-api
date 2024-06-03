from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, HydroponicSystem, SensorReading

admin.site.register(User, UserAdmin)
admin.site.register(HydroponicSystem)
admin.site.register(SensorReading)
