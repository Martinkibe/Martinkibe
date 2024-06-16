from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import VenueEvent, OnlineEvent, Booking

@receiver(post_save, sender=VenueEvent)
def create_booking_for_venue_event(sender, instance, created, **kwargs):
    if created:
        # Assuming the user is the organizer for now
        user = User.objects.get(username=instance.organizer_name)
        content_type = ContentType.objects.get_for_model(VenueEvent)
        Booking.objects.create(
            user=user,
            content_type=content_type,
            object_id=instance.id
        )

@receiver(post_save, sender=OnlineEvent)
def create_booking_for_online_event(sender, instance, created, **kwargs):
    if created:
        # Assuming the user is the organizer for now
        user = User.objects.get(username=instance.organizer_name)
        content_type = ContentType.objects.get_for_model(OnlineEvent)
        Booking.objects.create(
            user=user,
            content_type=content_type,
            object_id=instance.id
        )
