from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def organizer_dashboard(request):
    return render(request, 'organizer_dashboard.html')