from django.conf import settings
from django.db import models

class Club(models.Model):
    CATEGORY_CHOICES = (
        ('Academic', 'Academic Clubs'),
        ('Creative', 'Creative Clubs'),
        ('Diversity/Multicutural', 'Diversity Clubs'),
        ('Professional', 'Professional Clubs'),
        ('Religious', 'Religious Clubs'),
        ('Social Service', 'Social Service Clubs'),
        ('Sports', 'Sports Clubs'),
    )
    

    name = models.CharField(max_length=100, verbose_name='Club Name')
    email = models.EmailField(verbose_name='Club Email')
    meeting_type = models.CharField(max_length=100, default='On Campus', verbose_name='Hybrid ( On Campus & Virtual )')
    hybrid_link = models.URLField(blank=True, verbose_name='Hybrid Link ( If Applicable )')
    advisor_name = models.CharField(max_length=100, verbose_name='Advisor Name')
    advisor_email = models.EmailField(verbose_name='Advisor Email')
    club_room = models.CharField(max_length=100, verbose_name='Club Room')
    active = models.CharField(max_length=100, default='Active')
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    club_members = models.IntegerField(default=0, verbose_name='Number of Members')

    def __str__(self):
        return self.name
    
class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.club.name}'
