from django.shortcuts import render, redirect
from .models import Club
from .forms import ClubForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from myapp.models import CustomUser
from django.http import JsonResponse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from django.db import connection as con

def chart_view(request):
    query = """SELECT CC.club_id, CL.name, count(*) as club_members 
        FROM myapp_customuser_clubs CC
        INNER Join myapp_customuser CU
        On CC.customuser_id = CU.id
        Inner join clubs_club CL
        On CC.club_id = CL.id
        Group by cc.club_id, cl.name
        order by club_members desc
        """
    chartdata = pd.read_sql_query(query, con)
    
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(7, 7))
    sns.barplot(data=chartdata, x='club_members', y='name', ax=ax)

    # Save the plot as SVG file
    plt.savefig("client/images/seaborn_plot.svg", format='svg', bbox_inches='tight')
    # Render the plot in the template
    return render(request, 'data.html', {'plot_path': '/client/images/seaborn_plot.svg'})
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
