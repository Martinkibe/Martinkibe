from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .forms import OnlineEventForm, VenueEventForm, EventSearchForm
from .models import Booking, VenueEvent, OnlineEvent, EventCategory
from django.utils import timezone
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
    # Check if the user has already booked this online event
    event_already_booked = Booking.objects.filter(
        user=request.user,
        content_type=ContentType.objects.get_for_model(OnlineEvent),
        object_id=event.id
    ).exists()
    
    # Fetch more events logic here, for example:
    more_events = OnlineEvent.objects.exclude(id=pk)[:5]
    # start date to initiate the count down
    event_start_date = event.event_date.timestamp()
    context = {
        'event': event,
        'more_events': more_events,
        'event_start_date': event_start_date,
        'event_already_booked': event_already_booked,
    }
    return render(request, 'online_event.html', context)

def venue_event(request, pk):
    event = get_object_or_404(VenueEvent, id=pk)
    # Check if the user has already booked this online event
    event_already_booked = Booking.objects.filter(
        user=request.user,
        content_type=ContentType.objects.get_for_model(OnlineEvent),
        object_id=event.id
    ).exists()
    
    more_events = VenueEvent.objects.exclude(id=pk)[:5]  # Exclude current event and limit to 5 more events
    # start date to initiate the count down
    event_start_date = event.event_date.timestamp()
    return render(request, 'venue_event.html', {'event': event, 'more_events': more_events, 'event_start_date': event_start_date, 'event_already_booked': event_already_booked,})



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
            try:
                event = form.save()
                messages.success(request, 'Online event created successfully!')
                return redirect('events:online_event', pk=event.pk)
            except Exception as e:
                messages.error(request, f'Error creating event: {e}')
                print(f'Error creating event: {e}')
        else:
            messages.error(request, 'There was an error with the form. Please correct the errors below.')
    else:
        form = OnlineEventForm()

    return render(request, 'create_online_event.html', {'form': form})

@login_required
@user_passes_test(is_organizer)
def create_venue_event(request):
    if request.method == 'POST':
        form = VenueEventForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                event = form.save()
                messages.success(request, 'Venue event created successfully!')
                return redirect('events:venue_event', pk=event.pk)
            except Exception as e:
                messages.error(request, f'Error creating event: {e}')
        else:
            messages.error(request, 'There was an error with the form. Please correct the errors below.')
    else:
        form = VenueEventForm()

    return render(request, 'create_venue_event.html', {'form': form})

@login_required
def book_event(request, event_type, event_id):
    # Determine the event model based on event_type
    if event_type == 'venue':
        event_model = VenueEvent
    elif event_type == 'online':
        event_model = OnlineEvent
    else:
        # Handle invalid event_type (optional)
        return redirect('home')  # Redirect to home or an error page
    
    # Retrieve the event instance
    event_instance = get_object_or_404(event_model, id=event_id)
    
    # Get the content type for the event model
    content_type = ContentType.objects.get_for_model(event_model)
    
    # Check if a booking already exists for this event and user
    existing_booking = Booking.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=event_instance.id
    ).exists()
    
    if existing_booking:
        # Handle case where booking already exists (optional)
        messages.error(request, 'You have already booked this event.')
        return redirect('events:events')
    
    # Create the Booking instance using signal
    booking = Booking.objects.create(
        user=request.user,
        booking_date=timezone.now(),  # Example: Use current time as booking date
        content_type=content_type,
        object_id=event_instance.id
    )
    
    # Redirect to a booking confirmation page with event details
    if event_type == 'venue':
        event_name = event_instance.event_name  # Adjust this based on your VenueEvent model
        event_date = event_instance.event_date.strftime('%a, %b %d, %Y at %I:%M %p')  # Example formatting
        event_location = event_instance.event_location 
        event_image = event_instance.event_image.url  # Assuming event_image is an ImageField in VenueEvent
        ticket_price = event_instance.ticket_price
        return redirect(reverse('events:booking_confirmation') + f'?event_name={event_name}&event_date={event_date}&location={event_location}&event_image={event_image}&ticket_price={ticket_price}')
    elif event_type == 'online':
        event_name = event_instance.event_name  # Adjust this based on your OnlineEvent model
        event_date = event_instance.event_date.strftime('%a, %b %d, %Y at %I:%M %p')  # Example formatting
        online_location = event_instance.event_url  # Assuming event_url is a field in OnlineEvent model
        event_image = event_instance.event_image.url  # Assuming event_image is an ImageField in OnlineEvent
        ticket_price = event_instance.ticket_price
        return redirect(reverse('events:booking_confirmation') + f'?event_name={event_name}&event_date={event_date}&location={online_location}&event_image={event_image}&ticket_price={ticket_price}')
    else:
        return redirect('events:events')  # Handle invalid event_type

def booking_confirmation(request):
    event_name = request.GET.get('event_name')
    event_date = request.GET.get('event_date')
    location = request.GET.get('location')
    event_image = request.GET.get('event_image')  # Get event image URL
    ticket_price = request.GET.get('ticket_price')  # Get ticket price
    context = {
        'event_name': event_name,
        'event_date': event_date,
        'location': location,
        'event_image': event_image,
        'ticket_price': ticket_price,
    }
    
    return render(request, 'booking_confirmed.html', context)