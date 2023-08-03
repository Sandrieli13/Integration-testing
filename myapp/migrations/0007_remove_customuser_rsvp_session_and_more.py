# Generated by Django 4.2.3 on 2023-07-19 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_mentor_user_alter_mentor_availability_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='rsvp_session',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='training_availability',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='rsvp_session',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='training_availability',
        ),
        migrations.AddField(
            model_name='mentee',
            name='availability',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='mentee',
            name='user',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mentee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mentor',
            name='major',
            field=models.CharField(default='N/A', max_length=100, verbose_name='Mentor Major'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='preferred_language',
            field=models.CharField(max_length=100, verbose_name='Preferred Language'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='emplid',
            field=models.IntegerField(default=0, verbose_name='EmplID'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Mentor First Name'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Mentor Last Name'),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='myapp.mentee')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='myapp.mentor')),
            ],
        ),
    ]
