from rest_framework.pagination import PageNumberPagination


class HydroponicSystemPagination(PageNumberPagination):
    page_size = 10


class SensorReadingPagination(PageNumberPagination):
    page_size = 20
