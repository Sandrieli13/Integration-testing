from django.conf import settings
from django.db import models

class Event(models.Model):
    eventName = models.CharField(max_length=100, verbose_name='Club Name')
    eventDate = models.DateField()
    eventLocation = models.CharField(max_length=100, verbose_name='Advisor Name')
    eventTime = models.TimeField()

    def __str__(self):
        return self.name
    
class Goer(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     club = models.ForeignKey(Event, on_delete=models.CASCADE)

     def __str__(self):
         return f'{self.user.username} - {self.club.name}'


# Create your models here.
