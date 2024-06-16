from django.urls import path, include
from .views import organizer_dashboard

urlpatterns = [
    path('', include('allauth.urls')),
    path('organizer-dashboard/', organizer_dashboard, name='organizer_dashboard'),
]
