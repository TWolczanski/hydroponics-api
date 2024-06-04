import django_filters as filters
from core.models import HydroponicSystem, SensorReading


class HydroponicSystemFilter(filters.FilterSet):
    class Meta:
        model = HydroponicSystem
        fields = {
            "name": ["exact"],
            "plant_count": ["exact", "gte", "lte"],
            "created_at": ["exact", "gte", "lte"],
        }


class SensorReadingFilter(filters.FilterSet):
    class Meta:
        model = SensorReading
        fields = {
            "ph": ["exact", "gte", "lte"],
            "water_temp": ["exact", "gte", "lte"],
            "tds": ["exact", "gte", "lte"],
            "hydroponic_system": ["exact"],
            "created_at": ["exact", "gte", "lte"],
        }
