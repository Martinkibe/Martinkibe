from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class EventCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class VenueEvent(models.Model):
    event_name = models.CharField(max_length=200)
    categories = models.ManyToManyField(EventCategory)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_duration = models.DurationField()
    organizer_name = models.CharField(max_length=100)
    organizer_email = models.EmailField()
    organizer_phone = models.CharField(max_length=15)
    event_location = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    venue_address = models.TextField()

    def __str__(self):
        return self.event_name


class OnlineEvent(models.Model):
    event_name = models.CharField(max_length=200)
    categories = models.ManyToManyField(EventCategory)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_duration = models.DurationField()
    organizer_name = models.CharField(max_length=100)
    organizer_email = models.EmailField()
    organizer_phone = models.CharField(max_length=15)
    event_url = models.URLField()

    def __str__(self):
        return self.event_name


class Booking(models.Model):
    event_type_choices = [
        ('Venue', 'Venue'),
        ('Online', 'Online'),
    ]

    event_type = models.CharField(max_length=10, choices=event_type_choices)
    event_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['event_type', 'event_id']

    def __str__(self):
        return f'{self.user.username} booked {self.event_type} event with ID {self.event_id}'
    
    
    
    
    
    