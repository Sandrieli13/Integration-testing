from django.shortcuts import render,reverse
from django.http import HttpResponse
from .models import Majors, Courses, Semester
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
import pandas as pd
import json
import csv  
import os
from django.contrib.staticfiles import finders
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
    csv_files = [
        "S&E_technologies_associates_degrees",
        "Science_and_other_S&E_technologies",
        "Computer_Science_in_Associate's_Degrees_awarded_data",
        "Enrollment data for CIS Major",
        "Enrollment data for CNT Major",
        "Enrollment_data_for_CIS_department",
        "Enrollment data for CS Major",
        "Graduation data for CIS major",
        "Graduation data for CNT major",
        "Graduation data for CS major",
        "Graduation_data_or_CIS_department",
    ]

    return render(request, 'DataAnalysisPage.html', {'csv_files': csv_files})
def get_csv_data(request, file_name=None):
    if file_name is None:
        file_name = "default.csv"

    # Construct the file path for the requested CSV file
    csv_file_path = os.path.join('/static', file_name)

    try:
        with open(csv_file_path, 'r') as csv_file:
            # Process the CSV data and convert it to JSON format
            csv_reader = csv.DictReader(csv_file)
            csv_data = [row for row in csv_reader]

            # Convert the CSV data to JSON
            json_data = json.dumps(csv_data)

            # Return the JSON data as the response
            return HttpResponse(json_data, content_type='application/json')
    except FileNotFoundError:
        response_data = {"error": f"CSV file '{file_name}' not found."}
        return HttpResponse(json.dumps(response_data), content_type='application/json')