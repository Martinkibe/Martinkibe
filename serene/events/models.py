from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='type_images')
    
    class Meta:
        verbose_name = 'type'
        verbose_name_plural = 'types'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('events:type-detail', kwargs={'pk': self.pk})
    
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField('Details')
    venue = models.CharField(max_length=200)
    date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='events')
    organiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending', blank=True)
    num_of_attendees = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['date', 'time']

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def get_number_of_attendees(self):
        return self.attendees.all().count()

    def get_comments_number(self):
        return self.comments.all().count()


