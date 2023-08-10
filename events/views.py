from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your tests here.
def events_list_view(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    events = Event.objects.all()
    user_events = request.user.events.all()
    return render(request, 'events.html', {'events': events, 'user_events': user_events})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    if event in user.events.all():
        user.events.remove(event)
        joined = False
    else:
        user.events.add(event)
        joined = True

    data = {
        'joined': joined
    }

    return JsonResponse(data)