from django import forms
from .models import OnlineEvent, VenueEvent

class OnlineEventForm(forms.ModelForm):
    class Meta:
        model = OnlineEvent
        fields = ['event_name', 'event_description', 'event_date', 'event_time', 'event_duration', 'organizer_name', 'organizer_email', 'organizer_phone', 'event_url']

class VenueEventForm(forms.ModelForm):
    class Meta:
        model = VenueEvent
        fields = ['event_name', 'event_description', 'event_date', 'event_time', 'event_duration', 'organizer_name', 'organizer_email', 'organizer_phone', 'event_location', 'venue_name', 'venue_address']