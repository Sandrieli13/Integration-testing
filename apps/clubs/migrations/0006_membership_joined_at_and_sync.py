# Generated manually: audit trail + unique membership; backfill from legacy M2M.

from django.db import migrations, models
from django.utils import timezone


def dedupe_memberships(apps, schema_editor):
    Membership = apps.get_model("clubs", "Membership")
    db_alias = schema_editor.connection.alias
    seen = set()
    for m in Membership.objects.using(db_alias).all().order_by("id"):
        key = (m.user_id, m.club_id)
        if key in seen:
            m.delete()
        else:
            seen.add(key)


def backfill_from_user_clubs_m2m(apps, schema_editor):
    CustomUser = apps.get_model("myapp", "CustomUser")
    Membership = apps.get_model("clubs", "Membership")
    db_alias = schema_editor.connection.alias
    Through = CustomUser.clubs.through
    now = timezone.now()
    for row in Through.objects.using(db_alias).all():
        _, created = Membership.objects.using(db_alias).get_or_create(
            user_id=row.customuser_id,
            club_id=row.club_id,
            defaults={"joined_at": now},
        )
        if not created:
            continue


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0005_delete_mentee"),
        ("myapp", "0011_customuser_events"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="joined_at",
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
        migrations.RunPython(dedupe_memberships, noop_reverse),
        migrations.RunPython(backfill_from_user_clubs_m2m, noop_reverse),
        migrations.RunPython(dedupe_memberships, noop_reverse),
        migrations.AddConstraint(
            model_name="membership",
            constraint=models.UniqueConstraint(
                fields=("user", "club"),
                name="clubs_membership_user_club_uniq",
            ),
        ),
    ]
