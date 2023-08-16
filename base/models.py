from django.db import models
from django.utils import timezone

class Majors(models.Model):
    major_id = models.IntegerField(primary_key=True)
    major_name = models.CharField(max_length=100)

class Courses(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=100)
    major_id = models.IntegerField()
    credits = models.IntegerField()

def get_default_major_id():
    return Majors.objects.get(pk=1).major_id

class Semester(models.Model):
    semester_id = models.IntegerField()
    major = models.ForeignKey(Majors, on_delete=models.CASCADE, default=1)
    course1 = models.ForeignKey(Courses, related_name='course1_semester', on_delete=models.CASCADE, null=True)
    course2 = models.ForeignKey(Courses, related_name='course2_semester', on_delete=models.CASCADE, null=True)
    course3 = models.ForeignKey(Courses, related_name='course3_semester', on_delete=models.CASCADE, null=True)
    course4 = models.ForeignKey(Courses, related_name='course4_semester', on_delete=models.CASCADE, null=True)
    course5 = models.ForeignKey(Courses, related_name='course5_semester', on_delete=models.CASCADE, null=True)

    total_credits = models.IntegerField()

    class Meta:
        ordering = ['major', 'semester_id']
        unique_together = (('semester_id', 'major'),)

    def __str__(self):
        return f'Semester {self.semester_id} - Major {self.major.major_name}'

class IndividualAndSociety(models.Model):
    id = models.AutoField(primary_key=True)
    credit = models.IntegerField()
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        db_table = 'Individual and Society'

class USExperienceInItsDiversity(models.Model):
    id = models.AutoField(primary_key=True)
    credit = models.IntegerField()
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        db_table = 'US Experience In ItsDiversity'

class WorldCulturesAndGlobalIssues(models.Model):
    id = models.AutoField(primary_key=True)
    credit = models.IntegerField()
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        db_table = 'World Cultures And GlobalIssues'


class ProgramElectives(models.Model):
    id = models.AutoField(primary_key=True)
    credit = models.IntegerField()
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        db_table = 'Program Electives'
