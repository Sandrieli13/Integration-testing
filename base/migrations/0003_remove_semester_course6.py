# Generated by Django 4.2.3 on 2023-08-16 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_individualandsociety_programelectives_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='course6',
        ),
    ]