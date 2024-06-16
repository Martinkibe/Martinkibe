from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class OrganizerLoginAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_organizer:
            return reverse('organizer_dashboard')
        else:
            return reverse('events:events')  # Redirect non-organizer users to the home page