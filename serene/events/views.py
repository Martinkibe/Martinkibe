from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OnlineEventForm, VenueEventForm, EventSearchForm
from .models import Booking, VenueEvent, OnlineEvent, EventCategory
from .threads import set_current_request
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.urls import reverse

def is_organizer(user):
    return user.is_authenticated and user.is_organizer
# Create your views here.

# @login_required

def events(request):
    online_events = OnlineEvent.objects.all()
    venue_events = VenueEvent.objects.all()
    categories = EventCategory.objects.all()
    # Combine and sort events by event_date
    events = sorted(
        list(online_events) + list(venue_events),
        key=lambda event: event.event_date
    )
    
    # Limit to 8 listings
    limited_events = events[:8]
    
    return render(request, 'home.html', {
        'all_events': limited_events,
        'home_url': reverse('events:events'),
        'explore_url': reverse('events:all-events'),
        'categories': categories,
    })

def all_events(request):
    categories = EventCategory.objects.all()
    online_events = OnlineEvent.objects.all()
    venue_events = VenueEvent.objects.all()
    form = EventSearchForm()
    #  include URLs for each event's detail page
    events = sorted(
        list(online_events) + list(venue_events),
        key=lambda event: event.event_date
    )
    return render(request, 'explore_events.html', {'all_events': events,'home_url': reverse('events:events'),'explore_url': reverse('events:all-events'),'form': form, 'categories': categories})

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



def search_events(request):
    if request.method == 'GET':
        form = EventSearchForm(request.GET)
        if form.is_valid():
            category_slug = form.cleaned_data.get('category')
            event_type = form.cleaned_data.get('event_type')

            q = Q()

            if category_slug != '01':
                q &= Q(categories__slug=category_slug)

            if event_type == 'online_events':
                events = OnlineEvent.objects.filter(q)
            elif event_type == 'venue_events':
                events = VenueEvent.objects.filter(q)
            else:
                online_events = OnlineEvent.objects.filter(q)
                venue_events = VenueEvent.objects.filter(q)
                events = list(online_events) + list(venue_events)
            categories = EventCategory.objects.all()
            context = {
                'events': events,
                'form': form,
                'categories': categories,
            }
            return render(request, 'search_results.html', context)
    else:
        form = EventSearchForm()

    return render(request, 'search_results.html', {'form': form})

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