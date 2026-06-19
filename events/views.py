from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event


def event_list(request):
    tab = request.GET.get('tab', 'upcoming')
    today = timezone.now().date()

    if tab == 'past':
        events = Event.objects.filter(is_published=True, event_date__lt=today).order_by('-event_date')
    else:
        events = Event.objects.filter(is_published=True, event_date__gte=today).order_by('event_date')
        tab = 'upcoming'

    return render(request, 'site/events.html', {'events': events, 'tab': tab})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_published=True)
    return render(request, 'site/event_detail.html', {'event': event})
