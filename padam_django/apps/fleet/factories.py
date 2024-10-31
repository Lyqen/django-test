import factory
from faker import Faker

from padam_django.apps.geography.factories import PlaceFactory

from . import models


fake = Faker(['fr'])


class DriverFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('padam_django.apps.users.factories.UserFactory')

    class Meta:
        model = models.Driver


class BusFactory(factory.django.DjangoModelFactory):
    licence_plate = factory.LazyFunction(fake.license_plate)

    class Meta:
        model = models.Bus

class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory(PlaceFactory)
    arrival_time = factory.LazyFunction(fake.time)

    class Meta:
        model = models.BusStop

class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)

    @factory.post_generation
    def stops(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for stop in extracted:
                self.stops.add(stop)
        else:
            # Create default stops if none are provided
            stop1 = BusStopFactory()
            stop2 = BusStopFactory()
            self.stops.add(stop1, stop2)

    class Meta:
        model = models.BusShift