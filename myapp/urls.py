from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/mentor/', views.mentor_registration, name='mentor_registration'),
    path('register/mentee/', views.mentee_registration, name='mentee_registration'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('signout/', views.signout_view, name='signout'),
    path('mentors/', views.mentors_view, name='mentors'),
    path('demo/', views.demo_view, name='demo'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('matchmaking/', views.matchmaking_view, name='matchmaking'),
]
