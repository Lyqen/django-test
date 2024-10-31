from django.forms import ValidationError, ModelForm
from .models import BusShift

class BusShiftForm(ModelForm):
    class Meta:
        model = BusShift
        fields = ['bus', 'driver', 'stops']
        required = ['bus', 'driver', 'stops']

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        driver = cleaned_data.get('driver')
        stops = cleaned_data.get('stops')
        
        # Custom validation logic for stops
        if stops and stops.count() >= 2:
            start_time = stops.order_by('arrival_time').first().arrival_time
            end_time = stops.order_by('arrival_time').last().arrival_time
        else:
            raise ValidationError('At least two stops are required')
        
        # Custom validation logic for overlapping shifts
        for busshift in BusShift.objects.all():
            if busshift.bus == bus:
                if busshift.start_time < end_time and busshift.end_time > start_time:
                    raise ValidationError('This bus is already assigned to another shift during this time.')
            if busshift.driver == driver:
                if busshift.start_time < end_time and busshift.end_time > start_time:
                    raise ValidationError('This driver is already assigned to another shift during this time.')

        return cleaned_data