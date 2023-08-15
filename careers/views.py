from django.shortcuts import render, get_object_or_404
from .models import Major, Job, Course, Skill, Intern
from django.db.models import Q
from django.db import connection
from django.db.models import F
from django.db.models import Count
from operator import itemgetter

def home(request):
    return render(request, 'home.html')

def page1(request):
    if request.method == 'POST':
        major_id = request.POST['major']
        major = get_object_or_404(Major, pk=major_id)
        return render(request, 'page1.html', {'major': major})
    else:
        majors = Major.objects.all()
        return render(request, 'page1.html', {'majors': majors})

def page2(request):
    if request.method == 'POST':
        major_id = request.POST['major']
        job_id = request.POST['job']
        major = get_object_or_404(Major, pk=major_id)
        job = get_object_or_404(Job, pk=job_id)

        # Get skills of the major and the job
        major_skills = major.skills.all()
        job_skills = job.skills.all()

        # Calculate mismatched skills and gap fillers
        mismatched_skills = job_skills.difference(major_skills)
        print("\n \n mismatched SKILLS: \n",mismatched_skills, "\n type: ", type(mismatched_skills))

        skill_names = mismatched_skills

        skill_gap_mappin = {}

        for skill_name in skill_names:
            try:
                skill = Skill.objects.get(name=skill_name)
                skill_gap_mappin[skill_name] = skill.gapfiller
            except Skill.DoesNotExist:
                skill_gap_mappin[skill_name] = "Skill not found"

        # for skill_name, gap_name in skill_gap_mappin.items():
        #     print(f"Skill: {skill_name}", f"gap: {gap_name}")


        
        return render(request, 'page2.html', {
            'major': major,
            'job': job,
            'major_skills': major_skills,
            'job_skills': job_skills,
            'mismatched_skills': mismatched_skills,
            'gapfilling': skill_gap_mappin.items(),
        })
    else:
        majors = Major.objects.all()
        jobs = Job.objects.all()
        return render(request, 'page2.html', {'majors': majors, 'jobs': jobs})




def page3(request):
    majors = Major.objects.all()
    skills = Skill.objects.all()
    courses = Course.objects.all()
    internships = Intern.objects.all()

    if request.method == 'POST':
        selected_major_id = request.POST.get('major')
        selected_major = Major.objects.get(pk=selected_major_id)

        selected_skills_ids = request.POST.getlist('selected_skills')
        selected_courses_ids = request.POST.getlist('selected_courses')
        internship_query = request.POST.get('internship')

        selected_skills = Skill.objects.filter(pk__in=selected_skills_ids)
        selected_courses = Course.objects.filter(pk__in=selected_courses_ids)

        if internship_query:
            internships = internships.filter(title__icontains=internship_query)

        # Case 1: Compare with all major skills and courses
        case_1_results = compare_internships(selected_major.skills.all(), selected_skills, selected_courses, internships)

        # Case 2: Compare with selected major skills and courses
        case_2_results = compare_internships(selected_skills, selected_skills, selected_courses, internships)

        return render(request, 'page3.html', {
            'majors': majors,
            'skills': skills,
            'courses': courses,
            'selected_skills': selected_skills,
            'selected_courses': selected_courses,
            'case_1_results': case_1_results,
            'case_2_results': case_2_results,
        })

    return render(request, 'page3.html', {'majors': majors, 'skills': skills, 'courses': courses})

def compare_internships(ref_skills, selected_skills, selected_courses, internships):
    results = []

    for internship in internships:
        intern_skills = internship.skills.all()
        intern_courses = internship.courses.all()

        common_skills = selected_skills.intersection(intern_skills)
        common_courses = selected_courses.intersection(intern_courses)

        skills_ratio = len(common_skills) / len(ref_skills)
        courses_ratio = len(common_courses) / len(selected_courses)

        results.append({
            'internship': internship,
            'common_skills': common_skills,
            'common_courses': common_courses,
            'skills_ratio': skills_ratio,
            'courses_ratio': courses_ratio,
        })

    return results



from django.http import JsonResponse

def get_internship_suggestions(request):
    query = request.GET.get('query')

    if not query:
        return JsonResponse([], safe=False)  # Return an empty list if query is empty
    
    # Use Q objects to perform a case-insensitive search
    suggestions = Intern.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))[:5]
    suggestion_list = [internship.title for internship in suggestions]
    return JsonResponse(suggestion_list, safe=False)

def get_skill_suggestions(request):
    query = request.GET.get('query')
    suggestions = Skill.objects.filter(name__icontains=query)[:5]
    suggestion_list = [skill.name for skill in suggestions]
    return JsonResponse(suggestion_list, safe=False)

def get_course_suggestions(request):
    query = request.GET.get('query')
    suggestions = Course.objects.filter(name__icontains=query)[:5]
    suggestion_list = [course.name for course in suggestions]
    return JsonResponse(suggestion_list, safe=False)