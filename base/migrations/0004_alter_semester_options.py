# Generated by Django 4.2.3 on 2023-08-16 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_semester_course6'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ['semester_id']},
        ),
    ]