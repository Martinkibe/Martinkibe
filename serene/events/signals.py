from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Booking
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

User = get_user_model()

@receiver(post_save, sender=Booking)
def send_booking_confirmation_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        event_content_type = instance.content_type
        event_object_id = instance.object_id
        
        # Determine the event model based on the content type
        event_model = event_content_type.model_class()
        event = event_model.objects.get(id=event_object_id)
        
        # Send booking confirmation email with HTML content
        subject = f'Booking Confirmation for {event}'
        sender_email = settings.EMAIL_HOST_USER  # Replace with your actual sender email
        # Retrieve the booking date
        booking_date = instance.booking_date.strftime('%m/%d/%Y')  # Format as needed
        
        context = {
            'user': user,
            'event': event,
            'booking_date': booking_date,
        }
        
        # Render HTML content from template
        html_message = render_to_string('emails/booking_confirmation_email.html', context)
        
        # Create plain text version (optional)
        plain_message = strip_tags(html_message)
        
        # Example of sending email using EmailMultiAlternatives for HTML content
        email = EmailMultiAlternatives(subject, plain_message, sender_email, [user.email])
        email.attach_alternative(html_message, "text/html")
        email.send()
