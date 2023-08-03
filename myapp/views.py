from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm, UserEditForm, UserMentor, UserMentee
from .models import Mentee, Mentor, CustomUser
from operator import attrgetter
from django.core.exceptions import ObjectDoesNotExist


def signout_view(request):
    logout(request)
    return redirect('index')

def signin_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Replace 'home' with the name of your home page URL pattern
            else:
                return render(request, 'signin.html', {'error': 'Invalid credentials'})
        else:
            return render(request, 'signin.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')  # Replace 'signin' with your sign-in URL name
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def mentor_registration(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    user = request.user
    mentor = Mentor.objects.filter(user=user).first()

    if request.method == 'POST':
        form = UserMentor(request.POST, instance=user)
        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.is_mentee = False
            mentor.is_mentor = True

            mentor.save()
            return redirect('matchmaking')  # Replace 'matchmaking' with the appropriate URL name for the matchmaking view
    else:
        form = UserMentor(instance=user)

    return render(request, 'mentor_registration.html', {'form': form})

def mentee_registration(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    user = request.user
    mentee = Mentee.objects.filter(user=user).first()

    if request.method == 'POST':
        form = UserMentee(request.POST, instance=user)
        if form.is_valid():
            mentee = form.save(commit=False)
            mentee.is_mentee = True
            mentee.is_mentor = False

            mentee.save()
            return redirect('matchmaking')  # Replace 'matchmaking' with the appropriate URL name for the matchmaking view
    else:
        form = UserMentee(instance=user)

    return render(request, 'mentee_registration.html', {'form': form})

def edit_profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace 'profile' with the name of your profile URL pattern
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def index(request):
    return render(request, 'home.html')

def mentors_view(request):
    return render(request, 'mentors.html')

def demo_view(request):
    return render(request, 'demo.html')



def matchmaking_view(request):
    user = request.user

    if user.is_mentee:
        # If the current user is a mentee, fetch all users who are mentors (is_mentor=True)
        mentors = CustomUser.objects.filter(is_mentor=True).exclude(id=user.id)

        # Calculate matching points for each mentor
        for mentor in mentors:
            mentor.matching_points = calculate_matching_points(user, mentor)

        # Sort mentors based on matching points in descending order
        mentors = sorted(mentors, key=attrgetter('matching_points'), reverse=True)

        context = {
            'user': user,
            'mentors': mentors,
        }
        return render(request, 'matchmaking.html', context)

    elif user.is_mentor:
        # If the current user is a mentor, fetch all users who are mentees (is_mentee=True)
        mentees = CustomUser.objects.filter(is_mentee=True).exclude(id=user.id)

        # Calculate matching points for each mentee
        for mentee in mentees:
            mentee.matching_points = calculate_matching_points(user, mentee)

        # Sort mentees based on matching points in descending order
        mentees = sorted(mentees, key=attrgetter('matching_points'), reverse=True)

        context = {
            'user': user,
            'mentees': mentees,
        }
        return render(request, 'matchmaking.html', context)

    # If the user is not a mentor or mentee, display an appropriate message or redirect as needed
    return render(request, 'matchmaking_not_available.html')

def calculate_matching_points(user, other_user):
    # Implement your matching points logic here
    # You can compare fields like major, preferred_language, availability, etc.
    points = 0
    if user.major == other_user.major:
        points += 2
    if user.preferred_language == other_user.preferred_language:
        points += 1
    # Add more criteria and calculate points accordingly
    return points