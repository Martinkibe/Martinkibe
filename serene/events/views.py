from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OnlineEventForm, VenueEventForm
from .models import Booking, VenueEvent, OnlineEvent
from .threads import set_current_request
from django.contrib.auth.decorators import user_passes_test
from itertools import chain

def is_organizer(user):
    return user.is_authenticated and user.is_organizer
# Create your views here.

# @login_required
def events(request):
    return render(request, 'home.html')

def all_events(request):
    online_events = OnlineEvent.objects.all()
    venue_events = VenueEvent.objects.all()
    #  include URLs for each event's detail page
    events = sorted(
        list(online_events) + list(venue_events),
        key=lambda event: event.event_date
    )
    return render(request, 'explore_events.html', {'all_events': events})

def online_event(request, pk):
    event = get_object_or_404(OnlineEvent, id=pk)
    # Fetch more events logic here, for example:
    more_events = OnlineEvent.objects.exclude(id=pk)[:5]
    # start date to initiate the count down
    event_start_date = event.event_date.timestamp()
    context = {
        'event': event,
        'more_events': more_events,
        'event_start_date': event_start_date,
    }
    return render(request, 'online_event.html', context)

def venue_event(request, pk):
    event = get_object_or_404(VenueEvent, id=pk)
    more_events = VenueEvent.objects.exclude(id=pk)[:5]  # Exclude current event and limit to 5 more events
    # start date to initiate the count down
    event_start_date = event.event_date.timestamp()
    return render(request, 'venue_event.html', {'event': event, 'more_events': more_events, 'event_start_date': event_start_date,})


def create(request):
    return render(request, 'create.html')
@login_required
@user_passes_test(is_organizer)
def create_online_event(request):
    if request.method == 'POST':
        form = OnlineEventForm(request.POST, request.FILES)
        if form.is_valid():
            set_current_request(request)
            form.save()
            return redirect('events:events')  # Update the redirection as needed
    else:
        form = OnlineEventForm()
    return render(request, 'create_online_event.html', {'form': form})

@login_required
@user_passes_test(is_organizer)
def create_venue_event(request):
    if request.method == 'POST':
        form = VenueEventForm(request.POST, request.FILES)
        if form.is_valid():
            set_current_request(request)
            form.save()
            return redirect('events:events')  # Update the redirection as needed
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