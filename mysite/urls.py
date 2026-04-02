"""Root URL configuration for mysite."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('', include('apps.clubs.urls')),
    path('', include('base.urls')),
    path(
        'careers/',
        include(('careers.urls', 'careers'), namespace='careers'),
    ),
    path('', include('events.urls')),
    path(
        'experiential/',
        include(
            ('experientiallearning.urls', 'experientiallearning'),
            namespace='experientiallearning',
        ),
    ),
]
