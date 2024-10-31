from django.contrib import admin
from . import models, forms


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = forms.BusShiftForm
