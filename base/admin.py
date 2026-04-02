from django.contrib import admin
from .models import Majors, Courses, Semester
from .models import (
    DepartmentMetric,
    IndividualAndSociety,
    ProgramElectives,
    USExperienceInItsDiversity,
    WorldCulturesAndGlobalIssues,
)
admin.site.register(Majors)
admin.site.register(Courses)
admin.site.register(Semester) 
admin.site.register(IndividualAndSociety)
admin.site.register(USExperienceInItsDiversity)
admin.site.register(WorldCulturesAndGlobalIssues)
admin.site.register(ProgramElectives)
admin.site.register(DepartmentMetric)