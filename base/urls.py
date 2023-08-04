from django.urls import path
from . import views

urlpatterns = [
    path('courselistpage/', views.courselistpage, name='courselistpage'),
    path('course_search/', views.course_search, name='coursesearch'),
    path('CampusInfo/', views.CampusInfo, name='CampusInfo'),
    path('coursePlanner/', views.coursePlanner, name='coursePlanner'),
    path('DataAnalysisPage/', views.DataAnalysisPage, name='DataAnalysisPage'),    
    path('get_csv_data/<str:file_name>/', views.get_csv_data, name='get_csv_data'),   
]