from django.urls import path
from . import views

urlpatterns = [
    path('courselistpage/', views.courselistpage, name='courselistpage'),
    path('course_search/', views.course_search, name='coursesearch'),
    path('CampusInfo/', views.CampusInfo, name='CampusInfo'),
    path('coursePlanner/', views.coursePlanner, name='coursePlanner'),
    path('DataAnalysisPage/', views.DataAnalysisPage, name='DataAnalysisPage'),
    path('fetch_courses/', views.fetch_courses, name='fetch_courses'),
    path('move_course/', views.move_course, name='move_course'),   
    path('electivecourses/', views.electivecourses, name='electivecourses'),
    path('studentprograms/', views.studentprograms, name='studentprograms'),
]
