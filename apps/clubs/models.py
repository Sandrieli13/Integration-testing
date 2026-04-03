from django.conf import settings
from django.db import models
from django.utils import timezone

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
    """Persists which users belong to which clubs (self-serve join or admin-assigned)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="club_memberships",
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "club"),
                name="clubs_membership_user_club_uniq",
            ),
        ]

    def __str__(self):
        return f"{self.user_id} · {self.club.name}"


class BmccClubsInfo(models.Model):
    """Cached snapshot of public BMCC student-clubs / OSA web content (see refresh_bmcc_clubs_info)."""

    intro_text = models.TextField(blank=True)
    highlights = models.JSONField(default=list)
    resource_links = models.JSONField(default=list)
    osa_email = models.CharField(max_length=254, blank=True)
    osa_phone = models.CharField(max_length=80, blank=True)
    osa_hours = models.CharField(max_length=500, blank=True)
    extra_notice = models.TextField(blank=True)
    raw_plain_text = models.TextField(blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    fetched_at = models.DateTimeField(null=True, blank=True)
    fetch_error = models.TextField(blank=True)

    class Meta:
        verbose_name = "BMCC clubs page snapshot"
        verbose_name_plural = "BMCC clubs page snapshots"

    def __str__(self) -> str:
        when = self.fetched_at.strftime("%Y-%m-%d %H:%M") if self.fetched_at else "never"
        return f"BMCC clubs snapshot ({when})"
