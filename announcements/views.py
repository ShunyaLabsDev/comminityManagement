from django.shortcuts import render
from .models import Announcement


def announcement_list(request):
    announcements = Announcement.objects.filter(is_published=True).order_by('-publish_date')
    return render(request, 'site/announcements.html', {'announcements': announcements})
