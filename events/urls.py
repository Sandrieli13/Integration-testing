from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.events_list_view, name='events'),
    path('events/join/<int:event_id>/', views.join_event, name='join_event'),
]
