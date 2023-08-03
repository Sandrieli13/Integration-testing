import csv
from django.conf import settings
from django.db import models
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

from apps.clubs.models import Club

def import_clubs():
    csv_file = 'clubs.csv'  # Update with the correct CSV file name or path

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            club = Club(
                name=row['Club Name'],
                email=row['Club Email'],
                meeting_type=row['Hybrid ( On Campus & Virtual )'],
                hybrid_link=row.get('Hybrid Link ( If Applicable )', ''),
                advisor_name=row['Advisor Name'],
                advisor_email=row['Advisor Email'],
                club_room=row['Club Room'],
                active=row.get('Active', 'Active')
            )
            club.save()

if __name__ == '__main__':
    import_clubs()
