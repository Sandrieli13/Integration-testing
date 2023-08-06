from django.shortcuts import render,reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Majors, Courses, Semester
from .models import Majors, Courses, Semester
from .models import IndividualAndSociety, USExperienceInItsDiversity, WorldCulturesAndGlobalIssues, ProgramElectives
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
import json
import csv
import os
import io
from django.conf import settings
import base64
import matplotlib
matplotlib.use('Agg')  # Add this line before importing pyplot
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.template import loader
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd
import seaborn as sns
import logging
from django.core import serializers
# Create your views here.
def home(request):
    return render(request, 'home.html')

def courselistpage(request):
    majors = Majors.objects.all()
    courses = Courses.objects.all()
    semesters = Semester.objects.all()

    context = {
        'majors': majors,
        'courses': courses,
        'semesters': semesters,
    }

    return render(request, 'courselistpage.html', context)

def course_search(request):
    if request.method == 'POST':
        major_id = int(request.POST.get('major'))  # Convert to integer
        print("Major ID:", major_id)
        try:
            major = Majors.objects.get(pk=major_id)
            courses = Courses.objects.filter(major_id=major_id)
            total_courses = courses.count()
            courses_per_semester = 5
            total_semesters = (total_courses + courses_per_semester - 1) // courses_per_semester
            total_credits = sum(course.credits for course in courses)

            # Determine major type based on major_id
            is_computer_science = (major_id == 1)
            is_computer_info_systems = (major_id == 2)
            is_computer_network_technology = (major_id == 3)
            is_geographic_information_science = (major_id == 4)

            return render(request, 'course_search_result.html', {
                'major': major,
                'courses': courses,
                'total_courses': total_courses,
                'total_semesters': total_semesters,
                'total_credits': total_credits,
                'is_computer_science': is_computer_science,
                'is_computer_info_systems': is_computer_info_systems,
                'is_computer_network_technology': is_computer_network_technology,
                'is_geographic_information_science': is_geographic_information_science,
            })
        except Majors.DoesNotExist:
            return render(request, 'course_search_result.html', {'error_message': 'Major not found.'})

    # If it's a GET request or the form has not been submitted yet
    majors = Majors.objects.all()
    return render(request, 'course_search.html', {'majors': majors})

def CampusInfo(request):
    return render(request, 'CampusInfo.html')

 
 

def DataAnalysisPage(request, file_name=None):
    chart_files = {
        'csv/Enrollment data for CIS department.csv': 'Enrollment data for CIS department',
        'csv/Graduation data for CIS department.csv': 'Graduation data for CIS department',
        'csv/Enrollment data for CS Major.csv': 'Enrollment data for CS Major',
        'csv/Graduation data for CS major.csv': 'Graduation data for CS major',
        'csv/Enrollment data for CNT Major.csv': 'Enrollment data for CNT Major',
        'csv/Graduation data for CNT major.csv': 'Graduation data for CNT major',
        'csv/Enrollment data for CIS Major.csv': 'Enrollment data for CIS Major',
        'csv/Graduation data for CIS major.csv': 'Graduation data for CIS major',       
        
    }

    all_data = []
    for file_path, chart_name in chart_files.items():
        csv_file_path = os.path.join(settings.STATICFILES_DIRS[0], file_path)
        data = read_csv_file(csv_file_path)
        all_data.append((data, chart_name))

    return render(request, 'DataAnalysisPage.html', {'all_data': all_data})

def read_csv_file(csv_path):
    data = []
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            try:
                year = int(row[0])
                value = int(row[1])
                data.append([year, value])
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Error in CSV file: {csv_path}. Row: {row}")
                logger.error(e)
    return data
def fetch_courses(request):
    major_id = request.GET.get('majorId')
    courses = Courses.objects.filter(major_id=major_id)  # corrected line
    course_list = []

    for course in courses:
        course_list.append(f'<div class="item" data-course-id="{course.course_id}" data-credits="{course.credits}">{course.course_name}</div>')

    return HttpResponse(''.join(course_list))



def move_course(request):
    course_id = request.GET.get('courseId')
    course = get_object_or_404(Courses, course_id=course_id)

    # Perform the necessary operations to move the course
    # For example, you can update the course's status or move it to a different table

    return HttpResponse('Course moved successfully')

def coursePlanner(request):

    # Fetch the list of majors from the database
    majors = Majors.objects.all()

    # Fetch the list of courses from the database
    courses = Courses.objects.all()

    context = {
        'majors': majors,
        'courses': courses,
    }

    return render(request, 'coursePlanner.html', context)     

def electivecourses(request):
    individual_and_society_courses = IndividualAndSociety.objects.all()
    us_experience_courses = USExperienceInItsDiversity.objects.all()
    world_cultures_courses = WorldCulturesAndGlobalIssues.objects.all()
    program_electives = ProgramElectives.objects.all()

    context = {
        'individual_and_society_courses': individual_and_society_courses,
        'us_experience_courses': us_experience_courses,
        'world_cultures_courses': world_cultures_courses,
        'program_electives': program_electives,
    }

    return render(request, 'electivecourses.html', context)
def studentprograms(request):
    return render(request, 'studentprograms.html')