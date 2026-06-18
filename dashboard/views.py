from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from families.models import Family, Member
from events.models import Event
from announcements.models import Announcement
from gallery.models import GalleryImage


def is_staff(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff)
def dashboard_home(request):
    today = timezone.now().date()

    # Stats
    total_families = Family.objects.filter(is_active=True).count()
    total_members = Member.objects.filter(is_active=True).count()
    upcoming_events = Event.objects.filter(is_published=True, event_date__gte=today).count()
    total_announcements = Announcement.objects.filter(is_published=True).count()

    # Recent families
    recent_families = Family.objects.filter(is_active=True).order_by('-created_at')[:5]

    # Monthly registrations for chart (last 12 months)
    from datetime import date, timedelta
    import json
    months = []
    family_counts = []
    member_counts = []
    for i in range(11, -1, -1):
        d = today.replace(day=1) - timedelta(days=i * 28)
        month_name = d.strftime('%b %Y')
        months.append(month_name)
        fam_count = Family.objects.filter(
            created_at__year=d.year,
            created_at__month=d.month
        ).count()
        family_counts.append(fam_count)

    context = {
        'total_families': total_families,
        'total_members': total_members,
        'upcoming_events': upcoming_events,
        'total_announcements': total_announcements,
        'recent_families': recent_families,
        'months_json': json.dumps(months),
        'family_counts_json': json.dumps(family_counts),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_staff)
def family_list(request):
    families = Family.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'admin_panel/families.html', {'families': families})


@login_required
@user_passes_test(is_staff)
def family_add(request):
    from .forms import FamilyForm
    if request.method == 'POST':
        form = FamilyForm(request.POST, request.FILES)
        if form.is_valid():
            family = form.save()
            messages.success(request, f'કુટુંબ "{family.family_name}" સફળતાપૂર્વક ઉમેરવામાં આવ્યું!')
            return redirect('dashboard_families')
    else:
        form = FamilyForm()
    return render(request, 'admin_panel/family_form.html', {'form': form, 'title': 'Add Family / કુટુંબ ઉમેરો'})


@login_required
@user_passes_test(is_staff)
def family_edit(request, pk):
    from .forms import FamilyForm
    family = get_object_or_404(Family, pk=pk)
    if request.method == 'POST':
        form = FamilyForm(request.POST, request.FILES, instance=family)
        if form.is_valid():
            form.save()
            messages.success(request, 'કુટુંબ માહિતી અપડેટ થઈ!')
            return redirect('dashboard_families')
    else:
        form = FamilyForm(instance=family)
    return render(request, 'admin_panel/family_form.html', {'form': form, 'title': 'Edit Family / કુટુંબ સુધારો', 'family': family})


@login_required
@user_passes_test(is_staff)
def member_add(request, family_pk):
    from .forms import MemberForm
    family = get_object_or_404(Family, pk=family_pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.family = family
            member.save()
            messages.success(request, f'સભ્ય "{member.name}" ઉમેરાયા!')
            return redirect('dashboard_families')
    else:
        form = MemberForm()
    return render(request, 'admin_panel/member_form.html', {'form': form, 'family': family})


@login_required
@user_passes_test(is_staff)
def event_add(request):
    from .forms import EventForm
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'કાર્યક્રમ ઉમેરાયો!')
            return redirect('dashboard_home')
    else:
        form = EventForm()
    return render(request, 'admin_panel/event_form.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def announcement_add(request):
    from .forms import AnnouncementForm
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'જાહેરાત ઉમેરાઈ!')
            return redirect('dashboard_home')
    else:
        form = AnnouncementForm()
    return render(request, 'admin_panel/announcement_form.html', {'form': form})
