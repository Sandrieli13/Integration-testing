from django import forms
from .models import Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'email', 'meeting_type', 'hybrid_link', 'advisor_name', 'advisor_email', 'club_room', 'category']

