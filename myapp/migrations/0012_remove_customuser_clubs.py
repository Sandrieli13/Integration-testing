from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0011_customuser_events"),
        ("clubs", "0006_membership_joined_at_and_sync"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="clubs",
        ),
    ]
