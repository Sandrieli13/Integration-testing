from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'experientiallearning'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='experientiallearning/index.html'),
        name='index',
    ),
    path(
        'about/',
        TemplateView.as_view(template_name='experientiallearning/about.html'),
        name='about',
    ),
    path(
        'job-board/',
        TemplateView.as_view(template_name='experientiallearning/jobBoard.html'),
        name='job_board',
    ),
    path(
        'events/',
        TemplateView.as_view(template_name='experientiallearning/events.html'),
        name='events',
    ),
    path(
        'career-info/',
        TemplateView.as_view(template_name='experientiallearning/careerInfo.html'),
        name='career_info',
    ),
    path(
        'research/',
        TemplateView.as_view(template_name='experientiallearning/research.html'),
        name='research',
    ),
    path('register-events/', views.register_events_page, name='register_events'),
    path(
        'login/',
        TemplateView.as_view(template_name='experientiallearning/login.html'),
        name='login',
    ),
    path('login/submit/', views.login_submit, name='login_submit'),
    path('account/', views.account, name='account'),
    path(
        'my-account/',
        TemplateView.as_view(template_name='experientiallearning/myAccount3.html'),
        name='my_account',
    ),
    path(
        'my-account/submit/',
        views.student_intake_submit,
        name='student_intake_submit',
    ),
    path(
        'update/',
        TemplateView.as_view(template_name='experientiallearning/update.html'),
        name='update_profile',
    ),
    path('update/submit/', views.update_submit, name='update_submit'),
    path(
        'delete/',
        TemplateView.as_view(template_name='experientiallearning/delete.html'),
        name='delete_account',
    ),
    path('delete/submit/', views.delete_submit, name='delete_submit'),
    path('career-statistics/', views.career_statistics, name='career_statistics'),
]
