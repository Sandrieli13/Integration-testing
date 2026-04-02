from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClubForm
from .models import Club


def chart_view(request):
    """Club member counts without pandas/matplotlib (small disk footprint on PA)."""
    query = """
        SELECT CL.name, COUNT(*) AS club_members
        FROM myapp_customuser_clubs CC
        INNER JOIN myapp_customuser CU ON CC.customuser_id = CU.id
        INNER JOIN clubs_club CL ON CC.club_id = CL.id
        GROUP BY cc.club_id, CL.name
        ORDER BY club_members DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    max_members = max((r[1] for r in rows), default=1)
    clubs_chart = [
        {"name": r[0], "members": r[1], "pct": round(100 * r[1] / max_members)}
        for r in rows
    ]
    return render(request, "data.html", {"clubs_chart": clubs_chart})
@login_required
def profile_view(request):
    user = request.user
    clubs = user.clubs.all()
    events = user.events.all()
    return render(request, 'profile.html', {'user': user, 'clubs': clubs, 'events': events})
@login_required
def delete_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    club.delete()
    return redirect('/clubs')  # Redirect to the clubs list page after deleting the club

@login_required
def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    user = request.user
    if club in user.clubs.all():
        user.clubs.remove(club)
        joined = False
    else:
        user.clubs.add(club)
        joined = True

    data = {
        'joined': joined
    }

    return JsonResponse(data)


def clubs_list_view(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    clubs = Club.objects.all()
    user_clubs = request.user.clubs.all()
    categories = Club.objects.values_list('category', flat=True).distinct()
    return render(request, 'clubs_2.html', {'clubs': clubs, 'categories': categories, 'user_clubs': user_clubs})
    
def create_club_view(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/clubs')
    else:
        form = ClubForm()
    return render(request, 'create_club.html', {'form': form})

def edit_club(request, club_id):
    club = Club.objects.get(pk=club_id)
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect('/clubs')
    else:
        form = ClubForm(instance=club)
    return render(request, 'edit_club.html', {'form': form, 'club': club})
