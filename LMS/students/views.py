from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm
from .models import StudentProfile
from django.contrib import messages

# Create your views here.

def login_view(request):
    return render(request, 'students/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('students:profile_form')
    else:
        form = UserCreationForm()
    return render(request, 'students/signup.html', {'form': form})

@login_required
def profile_form(request):
    """Profile form view with improved handling"""
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'email': request.user.email or '',
            'full_name': request.user.get_full_name() or request.user.username
        }
    )

    if profile.is_profile_completed and not request.GET.get('edit'):
        return redirect('students:home')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_profile_completed = True
            profile.save()
            messages.success(request, 'Profile completed successfully!')
            return redirect('students:home')
    else:
        # Pre-fill form with social account data if available
        if created and request.user.socialaccount_set.exists():
            social_account = request.user.socialaccount_set.first()
            initial_data = {}
            if social_account.provider == 'google':
                initial_data = {
                    'full_name': social_account.extra_data.get('name', ''),
                    'email': social_account.extra_data.get('email', ''),
                }
            elif social_account.provider == 'github':
                initial_data = {
                    'full_name': social_account.extra_data.get('name', ''),
                    'email': social_account.extra_data.get('email', ''),
                    'github_url': social_account.extra_data.get('html_url', ''),
                }
            form = StudentProfileForm(instance=profile, initial=initial_data)
        else:
            form = StudentProfileForm(instance=profile)

    return render(request, 'students/profile_form.html', {'form': form})

@login_required
def home(request):
    """Home view that ensures profile completion"""
    try:
        profile = StudentProfile.objects.get(user=request.user)
        if not profile.is_profile_completed:
            messages.info(request, 'Please complete your profile to continue.')
            return redirect('students:profile_form')
    except StudentProfile.DoesNotExist:
        messages.info(request, 'Please complete your profile to continue.')
        return redirect('students:profile_form')
    
    return render(request, 'students/home.html')



