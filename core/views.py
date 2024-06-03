from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import HydroponicSystem, SensorReading
from core.serializers import HydroponicSystemSerializer, SensorReadingSerializer
from core.paginations import HydroponicSystemPagination, SensorReadingPagination
from core.permissions import IsHydroponicSystemOwner


class HydroponicSystemViewSet(ModelViewSet):
    serializer_class = HydroponicSystemSerializer
    pagination_class = HydroponicSystemPagination

    def get_queryset(self):
        user = self.request.user
        qs = HydroponicSystem.objects.filter(owner=user)

        if self.action == "retrieve":
            qs = qs.prefetch_recent_sensor_readings()

        return qs

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes.append(IsHydroponicSystemOwner)
        return [permission_class() for permission_class in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SensorReadingViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = SensorReadingSerializer
    pagination_class = SensorReadingPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SensorReading.objects.filter(hydroponic_system__owner=user)

    def perform_create(self, serializer):
        hydroponic_system = serializer.validated_data["hydroponic_system"]
        owner = HydroponicSystem.objects.get(pk=hydroponic_system).owner

        if self.request.user != owner:
            raise PermissionDenied("You are not the owner of the hydroponic system.")

        serializer.save()
