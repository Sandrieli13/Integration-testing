from django.db import models

# Create your models here.


class Major(models.Model):
	major = models.CharField(max_length=100)
	description = models.TextField( blank=True)
	jobs_From_Bmcc =models.ManyToManyField('job',blank=True)
	courses =models.ManyToManyField('course',blank=True)
	skills = models.ManyToManyField('skill',blank=True)

class Job(models.Model):
	job_title = models.CharField(max_length=100)
	skills = models.ManyToManyField('skill',blank=True)

class Course(models.Model):
	name = models.CharField(max_length=200)

class Skill(models.Model):
	name = models.CharField(max_length=200)
	gapfiller = models.TextField( blank=True)

	def __str__(self):
		return self.name

class Intern(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField( blank=True)
	link = models.URLField()
	courses =models.ManyToManyField('course',blank=True)
	skills = models.ManyToManyField('skill',blank=True)
	