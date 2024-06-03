from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from core.managers import HydroponicSystemManager


class User(AbstractUser):
    pass


class HydroponicSystem(models.Model):
    name = models.CharField(max_length=75, blank=True)
    description = models.CharField(max_length=800, blank=True)
    plant_count = models.PositiveIntegerField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hydroponic_systems"
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = HydroponicSystemManager()


class SensorReading(models.Model):
    ph = models.DecimalField(max_digits=4, decimal_places=2)
    water_temp = models.DecimalField(max_digits=5, decimal_places=2)
    tds = models.DecimalField(max_digits=7, decimal_places=2)
    hydroponic_system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="sensor_readings"
    )
    created_at = models.DateTimeField(default=timezone.now)
