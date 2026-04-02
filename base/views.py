from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .department_metrics import (
    ENROLLMENT_CHART_DEFINITIONS,
    read_year_value_csv,
    static_csv_abspath,
)
from .models import (
    Courses,
    DepartmentMetric,
    IndividualAndSociety,
    Majors,
    ProgramElectives,
    Semester,
    USExperienceInItsDiversity,
    WorldCulturesAndGlobalIssues,
)

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
    """
    Enrollment headcount time series only. DepartmentMetric ORM preferred, else CSV.
    """
    enrollment_data = []
    for spec in ENROLLMENT_CHART_DEFINITIONS:
        series_key = spec["series_key"]
        title = spec["title"]
        qs = DepartmentMetric.objects.filter(series_key=series_key).order_by("year")
        if qs.exists():
            data = [[row.year, row.value] for row in qs]
        else:
            csv_file_path = static_csv_abspath(spec["csv"])
            data = read_year_value_csv(csv_file_path)
        enrollment_data.append((data, title))

    enrollment_charts_json = [
        {"title": title, "points": data} for data, title in enrollment_data
    ]

    tableau_app_url = (
        "https://public.tableau.com/app/profile/bmcc.oiea/viz/BMCCDataDashboards/Welcome"
    )
    facts_url = (
        "https://www.bmcc.cuny.edu/iea/institutional-research-and-data-analytics/facts-and-statistics/"
    )

    return render(
        request,
        "DataAnalysisPage.html",
        {
            "enrollment_charts_json": enrollment_charts_json,
            "tableau_app_url": tableau_app_url,
            "facts_url": facts_url,
        },
    )


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
def checklist(request):
    return render(request, 'checklist.html')

