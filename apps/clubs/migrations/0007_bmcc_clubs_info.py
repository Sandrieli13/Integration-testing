from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0006_membership_joined_at_and_sync"),
    ]

    operations = [
        migrations.CreateModel(
            name="BmccClubsInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("intro_text", models.TextField(blank=True)),
                ("highlights", models.JSONField(default=list)),
                ("resource_links", models.JSONField(default=list)),
                ("osa_email", models.CharField(blank=True, max_length=254)),
                ("osa_phone", models.CharField(blank=True, max_length=80)),
                ("osa_hours", models.CharField(blank=True, max_length=500)),
                ("extra_notice", models.TextField(blank=True)),
                ("raw_plain_text", models.TextField(blank=True)),
                ("source_url", models.URLField(blank=True, max_length=500)),
                ("fetched_at", models.DateTimeField(blank=True, null=True)),
                ("fetch_error", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "BMCC clubs page snapshot",
                "verbose_name_plural": "BMCC clubs page snapshots",
            },
        ),
    ]
