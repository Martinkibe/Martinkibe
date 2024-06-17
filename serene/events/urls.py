from django.urls import path
from . import views
app_name = "events"

urlpatterns = [
    # events url
    path('', views.events, name="events"),
    # all events
    path('all-events/', views.all_events, name="all-events"),
    #  event Detail
    path('online-event/<int:pk>/', views.online_event, name='online_event_detail'),
    path('venue-event/<int:pk>/', views.venue_event, name='venue_event_detail'),
    # booking confirmed url
    path('booking-confirmed/<int:event_id>/<str:event_type>/', views.booking_confirmed, name="booking-confirmed"),
    # create
    path('create/', views.create, name="create"),
    # create online event url
    path('create-online-event/', views.create_online_event, name="create-online-event"),
    # create venue event url
    path('create-venue-event/', views.create_venue_event, name="create-venue-event"),
]