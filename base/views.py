from django.shortcuts import render
from django.http import HttpResponse
from .models import Majors, Courses, Semester
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

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



# def coursePlanner(request):
#     major_id = request.GET.get('majorId')
#     try:
#         major = Majors.objects.get(pk=major_id)
#         courses = Courses.objects.filter(major_id=major_id)

#         course_list = []
#         for course in courses:
#             course_list.append({
#                 'course_name': course.course_name,
#                 'credits': course.credits,
#             })

#         return JsonResponse(course_list, safe=False)  # Return the JSON response
#     except Majors.DoesNotExist:
#         return JsonResponse({'error': 'Major not found.'}, status=404)
def coursePlanner(request):
    major_id = request.GET.get('majorId')
    
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