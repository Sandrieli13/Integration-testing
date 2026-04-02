import json
from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from careers.tech_market_charts import get_tech_career_chart_series


def career_statistics(request):
    openings, salary, languages, chart_meta, scatter_points = get_tech_career_chart_series()
    return render(
        request,
        'experientiallearning/career_graphs.html',
        {
            'openings_json': json.dumps(openings),
            'salary_json': json.dumps(salary),
            'languages_json': json.dumps(languages),
            'scatter_json': json.dumps(scatter_points),
            'chart_meta': chart_meta,
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
