from django.urls import path
from . import views
app_name = "events"

urlpatterns = [
    # events url
    path('', views.events, name="events"),
]