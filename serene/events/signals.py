from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import VenueEvent, OnlineEvent, Booking
from .threads import get_current_request

User = get_user_model()

@receiver(post_save, sender=VenueEvent)
def create_booking_for_venue_event(sender, instance, created, **kwargs):
    request = get_current_request()
    if request and request.user.is_authenticated:
        user = request.user
        content_type = ContentType.objects.get_for_model(VenueEvent)
        Booking.objects.create(
            user=user,
            content_type=content_type,
            object_id=instance.id
        )

@receiver(post_save, sender=OnlineEvent)
def create_booking_for_online_event(sender, instance, created, **kwargs):
    request = get_current_request()
    if request and request.user.is_authenticated:
        user = request.user
        content_type = ContentType.objects.get_for_model(OnlineEvent)
        Booking.objects.create(
            user=user,
            content_type=content_type,
            object_id=instance.id
        )
