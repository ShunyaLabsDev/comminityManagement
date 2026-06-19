from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Family, Member, ContactInfo
from .forms import UserFamilyForm, UserMemberForm
from events.models import Event
from announcements.models import Announcement
from gallery.models import GalleryImage
from django.utils import timezone


# ──────────────────────────────────────────────
# PUBLIC PAGES
# ──────────────────────────────────────────────

# def home(request):
#     total_families = Family.objects.filter(is_active=True).count()
#     total_members = Member.objects.filter(is_active=True).count()
#     upcoming_events = Event.objects.filter(
#         event_date__gte=timezone.now().date()
#     ).order_by('event_date')[:3]
#     announcements = Announcement.objects.filter(
#         is_published=True
#     ).order_by('-publish_date')[:4]
#     gallery_preview = GalleryImage.objects.order_by('-created_at')[:6]
#     contact = ContactInfo.objects.first()

#     return render(request, 'public/home.html', {
#         'total_families': total_families,
#         'total_members': total_members,
#         'upcoming_events': upcoming_events,
#         'announcements': announcements,
#         'gallery_preview': gallery_preview,
#         'contact': contact,
#     })

def home(request):
    from django.http import HttpResponse
    import os

    info = []
    base = '/var/task/templates'
    info.append(f"templates/ contents: {os.listdir(base)}")
    
    public_path = os.path.join(base, 'public')
    if os.path.exists(public_path):
        info.append(f"templates/public/ contents: {os.listdir(public_path)}")
    else:
        info.append("templates/public/ DOES NOT EXIST")

    return HttpResponse("<br>".join(info))
 
def family_directory(request):
    families = Family.objects.filter(is_active=True).prefetch_related('members')

    search = request.GET.get('search', '')
    village = request.GET.get('village', '')
    gotra = request.GET.get('gotra', '')
    business = request.GET.get('business', '')

    if search:
        families = families.filter(
            Q(family_name__icontains=search) | Q(village__icontains=search)
        )
    if village:
        families = families.filter(village__icontains=village)
    if gotra:
        families = families.filter(gotra=gotra)
    if business:
        families = families.filter(business=business)

    sort = request.GET.get('sort', 'family_name')
    families = families.order_by('village', 'family_name') if sort == 'village' else families.order_by('family_name')

    paginator = Paginator(families, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    villages = Family.objects.filter(is_active=True).values_list('village', flat=True).distinct().order_by('village')

    from .models import GOTRA_CHOICES, BUSINESS_CHOICES
    return render(request, 'public/family_directory.html', {
        'page_obj': page_obj,
        'search': search,
        'village': village,
        'gotra': gotra,
        'business': business,
        'villages': villages,
        'gotra_choices': GOTRA_CHOICES,
        'business_choices': BUSINESS_CHOICES,
        'total_count': families.count(),
        'sort': sort,
    })


def family_detail(request, pk):
    family = get_object_or_404(Family, pk=pk, is_active=True)
    members = family.members.filter(is_active=True).order_by('relation')
    # Check if the logged-in user owns this family
    is_owner = request.user.is_authenticated and family.submitted_by == request.user
    return render(request, 'public/family_detail.html', {
        'family': family,
        'members': members,
        'is_owner': is_owner,
    })


def family_pdf(request, pk):
    family = get_object_or_404(Family, pk=pk, is_active=True)
    members = family.members.filter(is_active=True).order_by('relation')
    return render(request, 'public/family_pdf.html', {'family': family, 'members': members})


def contact_page(request):
    contact = ContactInfo.objects.first()
    return render(request, 'public/contact.html', {'contact': contact})


# ──────────────────────────────────────────────
# USER FAMILY MANAGEMENT (login required)
# ──────────────────────────────────────────────

@login_required
def my_family(request):
    """User's 'My Family' dashboard — shows their registered families"""
    families = Family.objects.filter(submitted_by=request.user, is_active=True).prefetch_related('members')
    return render(request, 'public/my_family.html', {'families': families})


@login_required
def my_family_register(request):
    """Let a logged-in user register a new family"""
    if request.method == 'POST':
        form = UserFamilyForm(request.POST, request.FILES)
        if form.is_valid():
            family = form.save(commit=False)
            family.submitted_by = request.user
            family.save()
            messages.success(
                request,
                f'🎉 તમારો પરિવાર "{family.family_name}" સફળતાપૂર્વક નોંધાઈ ગયો! '
                f'Family "{family.family_name}" registered successfully! '
                f'Now add your family members below.'
            )
            return redirect('my_family_members', pk=family.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill email and mobile from user profile
        initial = {'email': request.user.email}
        try:
            initial['mobile'] = request.user.profile.mobile
        except Exception:
            pass
        form = UserFamilyForm(initial=initial)

    return render(request, 'public/my_family_register.html', {'form': form})


@login_required
def my_family_edit(request, pk):
    """Let the owner edit their family details"""
    family = get_object_or_404(Family, pk=pk, is_active=True)

    # Only the owner or staff can edit
    if family.submitted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You are not allowed to edit this family.')
        return redirect('my_family')

    if request.method == 'POST':
        form = UserFamilyForm(request.POST, request.FILES, instance=family)
        if form.is_valid():
            form.save()
            messages.success(request, f'Family "{family.family_name}" updated successfully!')
            return redirect('my_family')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserFamilyForm(instance=family)

    return render(request, 'public/my_family_edit.html', {'form': form, 'family': family})


@login_required
def my_family_members(request, pk):
    """Let the owner manage members of their family"""
    family = get_object_or_404(Family, pk=pk, is_active=True)

    if family.submitted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You are not allowed to manage this family.')
        return redirect('my_family')

    members = family.members.filter(is_active=True).order_by('relation')

    if request.method == 'POST':
        form = UserMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.family = family
            member.save()
            messages.success(request, f'Member "{member.name}" added successfully!')
            return redirect('my_family_members', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserMemberForm()

    return render(request, 'public/my_family_members.html', {
        'family': family,
        'members': members,
        'form': form,
    })


@login_required
def my_family_member_delete(request, family_pk, member_pk):
    """Soft-delete a member from user's family"""
    family = get_object_or_404(Family, pk=family_pk, is_active=True)
    member = get_object_or_404(Member, pk=member_pk, family=family)

    if family.submitted_by != request.user and not request.user.is_staff:
        messages.error(request, 'Not allowed.')
        return redirect('my_family')

    if request.method == 'POST':
        member.is_active = False
        member.save()
        messages.success(request, f'Member "{member.name}" removed.')

    return redirect('my_family_members', pk=family_pk)
