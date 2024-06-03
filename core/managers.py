from django.db import models
from django.db.models import Prefetch


class HydroponicSystemQuerySet(models.QuerySet):
    def prefetch_recent_sensor_readings(self):
        from core.models import SensorReading

        qs = SensorReading.objects.order_by("-created_at")[:10]
        return self.prefetch_related(
            Prefetch("sensor_readings", queryset=qs, to_attr="recent_sensor_readings")
        )


HydroponicSystemManager = HydroponicSystemQuerySet.as_manager
