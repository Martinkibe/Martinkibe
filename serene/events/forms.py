from django import forms
from .models import OnlineEvent, VenueEvent, EventCategory

class OnlineEventForm(forms.ModelForm):
    class Meta:
        model = OnlineEvent
        fields = [
            'event_name', 'categories', 'event_description', 'event_date', 'event_time', 'event_duration',
            'organizer_name', 'organizer_email', 'organizer_phone', 'event_url', 'event_image',
            'ticket_price', 'ticket_quantity', 'tickets_sold', 'free_event'
        ]
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
            'event_url': 'Enter the URL for your event if applicable.',
            'ticket_price': 'Enter the price for each ticket.',
            'ticket_quantity': 'Enter the number of tickets available.',
            'tickets_sold': 'Enter the number of tickets sold (default is 0).',
            'free_event': 'Check this box if the event is free.'
        }

    def clean_ticket_quantity(self):
        ticket_quantity = self.cleaned_data.get('ticket_quantity')
        if ticket_quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative")
        if self.instance.pk:  # Check if it's an existing instance
            available_quantity = self.instance.ticket_quantity - self.instance.tickets_sold
            if ticket_quantity > available_quantity:
                raise forms.ValidationError("Not enough tickets available")
        return ticket_quantity

class VenueEventForm(forms.ModelForm):
    class Meta:
        model = VenueEvent
        fields = [
            'event_name', 'categories', 'event_description', 'event_date', 'event_time', 'event_duration',
            'organizer_name', 'organizer_email', 'organizer_phone', 'event_location', 'venue_name', 'venue_address', 'event_image',
            'ticket_price', 'ticket_quantity', 'tickets_sold', 'free_event'
        ]
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
            'event_location': 'Enter the location of your event.',
            'venue_name': 'Enter the name of the venue.',
            'venue_address': 'Enter the address of the venue.',
            'ticket_price': 'Enter the price for each ticket.',
            'ticket_quantity': 'Enter the number of tickets available.',
            'tickets_sold': 'Enter the number of tickets sold (default is 0).',
            'free_event': 'Check this box if the event is free.'
        }

    def clean_ticket_quantity(self):
        ticket_quantity = self.cleaned_data.get('ticket_quantity')
        if ticket_quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative")
        if self.instance.pk:  # Check if it's an existing instance
            available_quantity = self.instance.ticket_quantity - self.instance.tickets_sold
            if ticket_quantity > available_quantity:
                raise forms.ValidationError("Not enough tickets available")
        return ticket_quantity

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
        



        

    