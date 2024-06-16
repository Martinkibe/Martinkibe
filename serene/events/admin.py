from django.contrib import admin
from .models import EventCategory, VenueEvent, OnlineEvent, Booking

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(VenueEvent)
class VenueEventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'event_time', 'organizer_name', 'venue_name']
    filter_horizontal = ['categories']

@admin.register(OnlineEvent)
class OnlineEventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'event_time', 'organizer_name', 'event_url']
    filter_horizontal = ['categories']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'booking_date', 'object_id', 'booking_date']
    list_filter = ['booking_date']
