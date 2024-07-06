from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VenueEvent(models.Model):
    event_name = models.CharField(max_length=200)
    categories = models.ManyToManyField(EventCategory)
    event_description = models.TextField()
    event_date = models.DateTimeField()
    event_time = models.TimeField()
    event_duration = models.DurationField()
    organizer_name = models.CharField(max_length=100)
    organizer_email = models.EmailField()
    organizer_phone = models.CharField(max_length=15)
    event_location = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    venue_address = models.TextField()
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    # Ticket fields
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    ticket_quantity = models.PositiveIntegerField(default=10)
    tickets_sold = models.PositiveIntegerField(default=0)
    free_event = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name
    
    @property
    def event_type(self):
        return "venue"

class OnlineEvent(models.Model):
    event_name = models.CharField(max_length=200)
    categories = models.ManyToManyField(EventCategory)
    event_description = models.TextField()
    event_date = models.DateTimeField()
    event_time = models.TimeField()
    event_duration = models.DurationField()
    organizer_name = models.CharField(max_length=100)
    organizer_email = models.EmailField()
    organizer_phone = models.CharField(max_length=15)
    event_url = models.URLField()
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    # Ticket fields
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    ticket_quantity = models.PositiveIntegerField(default=10)
    tickets_sold = models.PositiveIntegerField(default=0)
    free_event = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name
    
    @property
    def event_type(self):
        return "online"


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
    
    
