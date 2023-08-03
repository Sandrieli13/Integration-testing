from django.contrib import admin
from .models import CustomUser
from .models import Mentee, Mentor

admin.site.register(CustomUser)
admin.site.register(Mentee)
admin.site.register(Mentor)
