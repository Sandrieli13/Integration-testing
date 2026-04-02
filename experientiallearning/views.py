import json
from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse


def _legacy_chart_data():
    openings = [
        {'label': 'Computer and Information Managers', 'y': 6683},
        {'label': 'Computer Programmers', 'y': 1867},
        {'label': 'Software Developers', 'y': 17595},
        {'label': 'Web Developer', 'y': 1565},
        {'label': 'Database Adminstrators', 'y': 940},
        {'label': 'Information Technology Project Managers', 'y': 3150},
        {'label': 'Business Intelligence Analysts', 'y': 1803},
    ]
    salary = [
        {'y': 87, 'label': 'Computer and Information Managers'},
        {'y': 45, 'label': 'Computer Programmers'},
        {'y': 61, 'label': 'Software Developers'},
        {'y': 35, 'label': 'Web Developers'},
        {'y': 53, 'label': 'Database Adminstrators'},
        {'y': 43, 'label': 'Information Technology Project Managers'},
        {'y': 59, 'label': 'Business Intelligence Analysts'},
    ]
    languages = [
        {'y': 65.36, 'label': 'JavaScript'},
        {'y': 55.08, 'label': 'HTML/CSS'},
        {'y': 49.43, 'label': 'SQL'},
        {'y': 48.07, 'label': 'Python'},
        {'y': 33.27, 'label': 'Java'},
        {'y': 27.98, 'label': 'C#'},
        {'y': 22.55, 'label': 'C++'},
        {'y': 20.87, 'label': 'PHP'},
        {'y': 19.24, 'label': 'C'},
        {'y': 11.15, 'label': 'Go'},
        {'y': 6.05, 'label': 'Ruby'},
        {'y': 4.91, 'label': 'Swift'},
        {'y': 4.66, 'label': 'R'},
        {'y': 4.10, 'label': 'Matlab'},
    ]
    return openings, salary, languages


def career_statistics(request):
    openings, salary, languages = _legacy_chart_data()
    return render(
        request,
        'experientiallearning/career_graphs.html',
        {
            'openings_json': json.dumps(openings),
            'salary_json': json.dumps(salary),
            'languages_json': json.dumps(languages),
        },
    )


def login_submit(request):
    if request.method != 'POST':
        return redirect('experientiallearning:login')
    cuny = (request.POST.get('cunyEMPLD') or '').strip()
    if not cuny:
        messages.warning(request, 'Please enter a CUNY EMPLID.')
        return redirect('experientiallearning:login')
    url = reverse('experientiallearning:account')
    return redirect(f'{url}?cunyEMPLD={quote(cuny)}')


def account(request):
    return render(
        request,
        'experientiallearning/account_display.html',
        {'cunyEMPLD': request.GET.get('cunyEMPLD', '').strip()},
    )


def update_submit(request):
    if request.method == 'POST':
        messages.info(
            request,
            'This form used MySQL (update_account.php). Wire it to a Django model to save changes.',
        )
    return redirect('experientiallearning:update_profile')


def delete_submit(request):
    if request.method == 'POST':
        messages.info(
            request,
            'This form used MySQL (delete_account.php). Implement deletion in Django before using in production.',
        )
    return redirect('experientiallearning:delete_account')


def student_intake_submit(request):
    if request.method == 'POST':
        messages.info(
            request,
            'Student intake used PHP/MySQL (studentIntake3.php). Use Django signup or a new model to persist data.',
        )
    return redirect('experientiallearning:my_account')


def register_events_page(request):
    if request.method == 'POST':
        messages.info(
            request,
            'Event registration used the legacy stack. Use the main site Events section (/events/) for Django-backed events.',
        )
        return redirect('experientiallearning:register_events')
    return render(request, 'experientiallearning/register_events.html')
