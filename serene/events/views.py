from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OnlineEventForm, VenueEventForm
from .models import Booking, VenueEvent, OnlineEvent
# Create your views here.

# @login_required
def events(request):
    return render(request, 'home.html')

def create(request):
    return render(request, 'create.html')

def create_online_event(request):
    if request.method == 'POST':
        form = OnlineEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:event-list')  # Update the redirection as needed
    else:
        form = OnlineEventForm()
    return render(request, 'create_online_event.html', {'form': form})

def create_venue_event(request):
    if request.method == 'POST':
        form = VenueEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:event-list')  # Update the redirection as needed
    else:
        form = VenueEventForm()
    return render(request, 'create_venue_event.html', {'form': form})

# def booking_confirmed(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     return render(request, 'booking_confirmed.html', {'event': event})

def booking_confirmed(request, event_id, event_type):
    if event_type == 'Venue':
        event = get_object_or_404(VenueEvent, id=event_id)
    elif event_type == 'Online':
        event = get_object_or_404(OnlineEvent, id=event_id)
    else:
        # Handle unknown event types
        event = None

    if event:
        is_booked = Booking.objects.filter(event_type=event_type, event_id=event_id).exists()
    else:
        is_booked = False

    return render(request, 'booking_confirmed.html', {'event': event, 'is_booked': is_booked})