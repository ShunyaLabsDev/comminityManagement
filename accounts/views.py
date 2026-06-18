from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def register_view(request):
    """User registration page"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'સ્વાગત છે, {user.first_name}! Registration successful. Welcome to Gujarati Samaj Portal!')
            return redirect('home')
        else:
            messages.error(request, 'કૃપા કરીને ફોર્મ ભૂલો સુધારો / Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view supporting username or email"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/dashboard/'
        return '/'

    def form_valid(self, form):
        messages.success(self.request, f'સ્વાગત છે, {form.get_user().first_name or form.get_user().username}! Welcome back!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Try authenticating with email if username lookup failed
        username_or_email = form.data.get('username', '')
        password = form.data.get('password', '')
        if username_or_email and password and '@' in username_or_email:
            try:
                user_obj = User.objects.get(email__iexact=username_or_email)
                user = authenticate(self.request, username=user_obj.username, password=password)
                if user is not None:
                    login(self.request, user)
                    messages.success(self.request, f'સ્વાગત છે, {user.first_name or user.username}! Welcome back!')
                    if user.is_staff or user.is_superuser:
                        return redirect('/dashboard/')
                    return redirect('/')
            except User.DoesNotExist:
                pass

        messages.error(self.request, 'Invalid username/email or password. Please try again.')
        return super().form_invalid(form)


@login_required
def logout_view(request):
    """Logout - confirm via POST, render confirmation via GET"""
    if request.method == 'POST':
        username = request.user.first_name or request.user.username
        logout(request)
        messages.success(request, f'આવજો, {username}! You have been logged out successfully.')
        return redirect('home')
    return render(request, 'accounts/logout_confirm.html')


@login_required
def profile_view(request):
    """User profile page"""
    return render(request, 'accounts/profile.html')
