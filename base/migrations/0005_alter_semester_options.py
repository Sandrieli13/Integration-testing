# Generated by Django 4.2.3 on 2023-08-16 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_semester_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ['major', 'semester_id']},
        ),
    ]