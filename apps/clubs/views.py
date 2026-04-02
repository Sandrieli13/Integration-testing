from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ClubForm
from .models import Club


def _staff(u):
    return u.is_authenticated and u.is_staff


@user_passes_test(_staff)
def chart_view(request):
    """Club member counts without pandas/matplotlib (small disk footprint on PA)."""
    query = """
        SELECT CL.name, COUNT(*) AS club_members
        FROM myapp_customuser_clubs CC
        INNER JOIN myapp_customuser CU ON CC.customuser_id = CU.id
        INNER JOIN clubs_club CL ON CC.club_id = CL.id
        GROUP BY CC.club_id, CL.name
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
    return render(request, "profile.html", {"user": user, "clubs": clubs, "events": events})


@user_passes_test(_staff)
@require_POST
def delete_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    club.delete()
    return redirect("clubs-list")


@login_required
@require_POST
def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    user = request.user
    if club in user.clubs.all():
        user.clubs.remove(club)
        joined = False
    else:
        user.clubs.add(club)
        joined = True

    members_count = club.members.count()
    return JsonResponse({"joined": joined, "members_count": members_count})


@login_required
def clubs_list_view(request):
    clubs = (
        Club.objects.annotate(member_count=Count("members", distinct=True))
        .order_by("category", "name")
    )
    user_clubs = list(request.user.clubs.all())
    user_club_ids = {c.id for c in user_clubs}
    categories = sorted(
        Club.objects.values_list("category", flat=True).distinct(),
    )
    return render(
        request,
        "clubs_2.html",
        {
            "clubs": clubs,
            "categories": categories,
            "user_clubs": user_clubs,
            "user_club_ids": user_club_ids,
        },
    )


@user_passes_test(_staff)
def create_club_view(request):
    if request.method == "POST":
        form = ClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clubs-list")
    else:
        form = ClubForm()
    return render(request, "create_club.html", {"form": form})


@user_passes_test(_staff)
def edit_club(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == "POST":
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect("clubs-list")
    else:
        form = ClubForm(instance=club)
    return render(request, "edit_club.html", {"form": form, "club": club})
