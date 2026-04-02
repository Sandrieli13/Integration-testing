from django.urls import path

from . import views

urlpatterns = [
    path('clubs/', views.clubs_list_view, name='clubs-list'),
    path('editClub/<int:club_id>/', views.edit_club, name='edit_club'),
    path('createClub', views.create_club_view, name='create_club'),
    path('clubs/join/<int:club_id>/', views.join_club, name='join_club'),
    path('clubs/delete/<int:club_id>/', views.delete_club, name='delete_club'),
    path('profile/', views.profile_view, name='profile'),
    path('data/', views.chart_view, name='charts'),
]
