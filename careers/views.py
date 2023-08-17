from django.shortcuts import render, get_object_or_404
from .models import Major, Job, Course, Skill, Intern
from django.db.models import Q
from django.db import connection
from django.db.models import F
from django.db.models import Count
from operator import itemgetter
from django.http import JsonResponse

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
    if request.method == 'POST':
        intern = request.POST.get('internship','')
        if not intern:
            intr_des = "Best Matched"

            major_id = request.POST['major']
            skills_id_list = request.POST.get('skill_ids', '').split(',')
            courses_id_list = request.POST.get('course_ids', '').split(',')
            intern_id = None

            selected_major = Major.objects.get(id__in=major_id)
            selected_skill_major = selected_major.skills.all()
            selected_skill_ids_major = Skill.objects.filter(id__in=selected_skill_major)
            selected_skill_names_major = [skill.name for skill in selected_skill_ids_major]

            selected_skills = Skill.objects.filter(id__in=skills_id_list)
            selected_skill_names = [skill.name for skill in selected_skills]

            selected_courses = Course.objects.filter(id__in=courses_id_list)
            selected_course_names = [course.name for course in selected_courses]

            combined_skills_list = list(set(selected_skill_names_major))+ selected_skill_names

            

            print('major ID:\n',major_id,'\n',"major skills:", selected_skill_names_major, "\n")
            print('skills IDs:\n',selected_skill_names,'\n')
            print('courses IDs:\n',selected_course_names ,'\n')
            print('intern ID:\n',intern_id,'\n')
            print('All Skills:\n ', combined_skills_list)

            intern_id = find_best_intern(combined_skills_list,selected_course_names)

            if intern_id:
                print("Best internship tite:", intern_id.title)
                print("Description:", intern_id.description)
                
                print("skills:")
                for skill in intern_id.skills.all():
                    print(skill.name)
                
                print("courses:")
                for course in intern_id.courses.all():
                    print(course.name)
        else:
            intr_des = "Selected"

            major_id = request.POST['major']
            skills_id_list = request.POST.get('skill_ids', '').split(',')
            courses_id_list = request.POST.get('course_ids', '').split(',')
            intern_id = Intern.objects.get(title=intern)

            selected_major = Major.objects.get(id__in=major_id)
            selected_skill_major = selected_major.skills.all()
            selected_skill_ids_major = Skill.objects.filter(id__in=selected_skill_major)
            selected_skill_names_major = [skill.name for skill in selected_skill_ids_major]

            selected_skills = Skill.objects.filter(id__in=skills_id_list)
            selected_skill_names = [skill.name for skill in selected_skills]

            selected_courses = Course.objects.filter(id__in=courses_id_list)
            selected_course_names = [course.name for course in selected_courses]

            combined_skills_list = list(set(selected_skill_names_major))+ selected_skill_names

            

            print('major ID:\n',major_id,'\n',"major skills:", selected_skill_names_major, "\n")
            print('skills IDs:\n',selected_skill_names,'\n')
            print('courses IDs:\n',selected_course_names ,'\n')
            print('intern ID:\n',intern_id,'\n')
            print('All Skills:\n ', combined_skills_list)

            if intern_id:
                print("Best internship tite:", intern_id.title)
                print("Description:", intern_id.description)
                
                print("skills:")
                for skill in intern_id.skills.all():
                    print(skill.name)
                
                print("courses:")
                for course in intern_id.courses.all():
                    print(course.name)

        return render(request, 'page3.html', {
            'majors': selected_major,
            'skills': selected_skill_names,
            'courses': selected_course_names,
            'intern': intern_id,
            'intr_des': intr_des,
            'done': 1,
        })

    else:

        return render(request, 'page3.html', {
            'majors': Major.objects.all(),
            'skills': Skill.objects.all(),
            'courses': Course.objects.all(),
        })

def calculate_skill_compat(skill1, skill2):
    if(skill1 == skill2):
        return 1
    else:
        return 0
    
def find_best_intern(combined_skills_list_names,courses_list_names):
    combined_skills_list = Skill.objects.filter(name__in=combined_skills_list_names)
    courses_list = Course.objects.filter(name__in=courses_list_names)
    best_intern = None
    best_score = 0
    
    for intern in Intern.objects.all():
        score = 0
        intern_skills = intern.skills.all()
        intern_courses = intern.courses.all()
        
        for skill in combined_skills_list:
            for intern_skill in intern_skills:
                compatibility_score = calculate_skill_compat(skill, intern_skill)
                score += compatibility_score

        for course in courses_list:
            for intern_course in intern_courses:
                compatibility_score = calculate_skill_compat(course, intern_course)
                score += compatibility_score
        
        if score > best_score:
            best_score = score
            best_intern = intern
            print('\n score +1')
    
    return best_intern




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
