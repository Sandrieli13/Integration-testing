from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('get_internship_suggestions/', views.get_internship_suggestions, name='get_internship_suggestions'),
    path('get_skill_suggestions/', views.get_skill_suggestions, name='get_skill_suggestions'),
    path('get_course_suggestions/', views.get_course_suggestions, name='get_course_suggestions'),

]