from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection, IntegrityError
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ClubForm
from .models import BmccClubsInfo, Club, Membership


def _staff(u):
    return u.is_authenticated and u.is_staff


@user_passes_test(_staff)
def chart_view(request):
    """Club member counts without pandas/matplotlib (small disk footprint on PA)."""
    query = """
        SELECT CL.name, COUNT(*) AS club_members
        FROM clubs_membership MM
        INNER JOIN clubs_club CL ON MM.club_id = CL.id
        GROUP BY MM.club_id, CL.name
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
    clubs = Club.objects.filter(memberships__user=user).distinct().order_by("name")
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
    membership = Membership.objects.filter(user=user, club=club).first()
    if membership:
        membership.delete()
        joined = False
    else:
        try:
            Membership.objects.create(user=user, club=club)
            joined = True
        except IntegrityError:
            joined = True

    members_count = Membership.objects.filter(club=club).count()
    club.club_members = members_count
    club.save(update_fields=["club_members"])

    wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if wants_json:
        return JsonResponse({"joined": joined, "members_count": members_count})

    if joined:
        messages.success(request, f"You joined {club.name}. Visit your profile anytime to see your clubs.")
    else:
        messages.info(request, f"You left {club.name}.")

    next_url = request.POST.get("next") or reverse("clubs-list")
    return redirect(next_url)


def clubs_list_view(request):
    clubs = (
        Club.objects.annotate(member_count=Count("memberships", distinct=True))
        .order_by("category", "name")
    )
    if request.user.is_authenticated:
        user_club_ids = set(
            Membership.objects.filter(user=request.user).values_list(
                "club_id", flat=True
            )
        )
    else:
        user_club_ids = set()
    bmcc_info = BmccClubsInfo.objects.filter(pk=1).first()
    return render(
        request,
        "clubs_2.html",
        {
            "clubs": clubs,
            "user_club_ids": user_club_ids,
            "bmcc_info": bmcc_info,
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
