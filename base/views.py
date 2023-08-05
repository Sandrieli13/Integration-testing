from django.shortcuts import render,reverse
from django.http import HttpResponse
from .models import Majors, Courses, Semester
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



def coursePlanner(request):
    print('loadCourseList() called')
    major_id = request.GET.get('majorId')
    print('Received major ID:', major_id)  # Add this line for debugging

    if not major_id:
        # Return an error JSON response if majorId is not provided in the request
        return JsonResponse({'error': 'Major ID not provided.'}, status=400)

    try:
        major = Majors.objects.get(pk=major_id)
        courses = Courses.objects.filter(major_id=major_id)

        course_list = []
        for course in courses:
            course_list.append({
                'course_name': course.course_name,
                'credits': course.credits,
            })

        return JsonResponse(course_list, safe=False)  # Return the JSON response
    except Majors.DoesNotExist:
        return JsonResponse({'error': 'Major not found.'}, status=404)
    except Exception as e:
        # Return an error JSON response if any other exception occurs
        return JsonResponse({'error': str(e)}, status=500)

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



def testDatachart(request):
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