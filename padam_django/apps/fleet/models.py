import datetime
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
    start_time = models.TimeField(default=datetime.time(0, 0))
    end_time = models.TimeField(default=datetime.time(0, 0))


    def clean(self):

        # Ensure no overlapping shifts for the same bus
        overlapping_shifts = BusShift.objects.filter(
            bus=self.bus,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        if overlapping_shifts.exists():
            raise ValidationError("This bus is already assigned to another shift during this time.")

        # Ensure no overlapping shifts for the same driver
        overlapping_shifts = BusShift.objects.filter(
            driver=self.driver,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        if overlapping_shifts.exists():
            raise ValidationError("This driver is already assigned to another shift during this time.")

    def update_times_based_on_stops(self):
        if self.stops.exists():
            self.start_time = self.stops.order_by('arrival_time').first().arrival_time
            self.end_time = self.stops.order_by('arrival_time').last().arrival_time

    def save(self, *args, **kwargs):
        
        if not self.pk:
            super().save(*args, **kwargs)
        
        # Update times based on stops
        self.update_times_based_on_stops()
        
        # Save the instance again to update the times
        super().save(*args, **kwargs)

    def __str__(self):
        return f"BusShift with {self.bus.licence_plate} driven by {self.driver.user.username} that begin at {self.start_time} and finish at {self.end_time} (id: {self.pk})"