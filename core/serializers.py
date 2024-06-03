from rest_framework import serializers
from core.models import HydroponicSystem, SensorReading


class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = ["id", "name", "description", "plant_count", "created_at"]
        read_only_fields = ["id", "created_at"]


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ["id", "ph", "water_temp", "tds", "hydroponic_system", "created_at"]
        read_only_fields = ["id", "created_at"]
