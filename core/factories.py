import factory
from core.models import HydroponicSystem, SensorReading, User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")

    class Meta:
        model = User


class HydroponicSystemFactory(factory.django.DjangoModelFactory):
    plant_count = factory.Faker("pyint", min_value=1, max_value=20)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = HydroponicSystem


class SensorReadingFactory(factory.django.DjangoModelFactory):
    ph = factory.Faker("pydecimal", right_digits=2, min_value=0, max_value=15)
    water_temp = factory.Faker("pydecimal", right_digits=2, min_value=0, max_value=100)
    tds = factory.Faker("pydecimal", right_digits=2, min_value=0, max_value=40000)
    hydroponic_system = factory.SubFactory(HydroponicSystemFactory)

    class Meta:
        model = SensorReading
