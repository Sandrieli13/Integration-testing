from django.conf import settings
from django.db import models

class Event(models.Model):
    eventName = models.CharField(max_length=100, verbose_name='Event Name')
    eventDate = models.DateField()
    eventLocation = models.CharField(max_length=100, verbose_name='Event Location')
    eventTime = models.TimeField()
    eventLink = models.CharField(max_length=100, default='link.com', verbose_name='Event Link')

    def __str__(self):
        return self.eventName
    
class Goer(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     event = models.ForeignKey(Event, on_delete=models.CASCADE)

     def __str__(self):
         return f'{self.user.username} - {self.event.eventName}'


# Create your models here.
