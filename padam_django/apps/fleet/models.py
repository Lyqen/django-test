from django.db import models
from django.forms import ValidationError

from padam_django.apps.geography.models import Place


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    arrival_time = models.TimeField()

    def __str__(self):
        return f"Bus stop to {self.place.name} at {self.arrival_time} (id: {self.pk})"
    
class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    stops = models.ManyToManyField(BusStop)

    def __str__(self):
        return f"Bus shift with {self.bus.licence_plate} driven by {self.driver.user.username} from {self.start_time} to {self.end_time}(id: {self.pk})"
    
    @property
    def start_time(self):
        """Start time of the shift."""
        if self.stops.exists():
            return self.stops.all().order_by('arrival_time').first().arrival_time
        return None

    @property
    def end_time(self):
        """End time of the shift."""
        if self.stops.exists():
            return self.stops.all().order_by('arrival_time').last().arrival_time
        return None

    @property
    def duration(self):
        """Duration time of the shift."""
        if self.start_time and self.end_time:
            return self.start_time - self.end_time
        else:
            return None