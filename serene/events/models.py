from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ['content_type', 'object_id']

    def __str__(self):
        return f'{self.user.username} booked {self.content_type} event with ID {self.object_id}'
