from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import HydroponicSystemViewSet, SensorReadingViewSet

router = routers.DefaultRouter()
router.register(
    r"hydroponic_systems", HydroponicSystemViewSet, basename="hydroponic-system"
)
router.register(r"sensor_readings", SensorReadingViewSet, basename="sensor-reading")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
]

urlpatterns += router.urls
