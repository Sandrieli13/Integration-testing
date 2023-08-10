"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import index, demo_view, edit_profile_view, matchmaking_view
from myapp.views import mentor_registration, mentee_registration, signin_view, signup_view
from apps.clubs import views
from apps.clubs.views import profile_view
from apps.clubs.views import chart_view
from myapp.views import signout_view
from apps.clubs.views import chart_view
from myapp.views import mentors_view
from django.contrib import admin
from django.urls import path, include
from events.views import events_list_view, join_event

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('register/mentor/', mentor_registration, name='mentor_registration'),
    path('register/mentee/', mentee_registration, name='mentee_registration'),
    path('clubs/', views.clubs_list_view, name='clubs-list'),
    path('editClub/<int:club_id>/', views.edit_club, name='edit_club'),
    path('createClub', views.create_club_view, name='create_club'),
    path('clubs/join/<int:club_id>/', views.join_club, name='join_club'),
    path('clubs/delete/<int:club_id>/', views.delete_club, name='delete_club'),
    path('signin/', signin_view, name='signin'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('signout/', signout_view, name='signout'),
    path('data/', chart_view, name='charts'),
    path('mentors/', mentors_view, name='mentors'),
    path('demo/', demo_view, name='demo'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('matchmaking/', matchmaking_view, name='matchmaking'),
    path('',include('base.urls')),
    path('events/', events_list_view, name='events'),
    path('events/join/<int:event_id>/', join_event, name='join_event'),
]
