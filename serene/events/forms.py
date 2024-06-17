from django import forms
from .models import OnlineEvent, VenueEvent, EventCategory

class OnlineEventForm(forms.ModelForm):
    class Meta:
        model = OnlineEvent
        fields = ['event_name', 'event_description', 'event_date', 'event_time', 'event_duration', 'organizer_name', 'organizer_email', 'organizer_phone', 'event_url', 'event_image']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'event_duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }
        help_texts = {
            'event_date': 'Select the date for your event.',
            'event_time': 'Enter the time for your event.',
            'event_duration': 'Enter the duration for your event in HH:MM format.',
            'organizer_name': 'Enter your name or the name of the event organizer.',
            'organizer_email': 'Enter your email or the email of the event organizer.',
            'organizer_phone': 'Enter your phone number or the phone number of the event organizer.',
            'event_url': 'Enter the URL for your event if applicable.'
        }

class VenueEventForm(forms.ModelForm):
    class Meta:
        model = VenueEvent
        fields = ['event_name', 'event_description', 'event_date', 'event_time', 'event_duration', 'organizer_name', 'organizer_email', 'organizer_phone', 'event_location', 'venue_name', 'venue_address', 'event_image']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'event_duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }
        
class EventSearchForm(forms.Form):
    category = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}), required=False)
    event_type = forms.ChoiceField(choices=[
        ('browse_all', 'Browse All'),
        ('online_events', 'Online Events'),
        ('venue_events', 'Venue Events')],
        widget=forms.Select(attrs={'class': 'selectpicker'}), required=False)

    def __init__(self, *args, **kwargs):
        super(EventSearchForm, self).__init__(*args, **kwargs)
        categories = EventCategory.objects.all()
        self.fields['category'].choices = [('01', 'All Categories')] + [(category.slug, category.name) for category in categories]