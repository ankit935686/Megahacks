from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm
from .models import StudentProfile
from django.contrib import messages
from instructor.models import FriendRequest

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
            
        # Add this to get pending requests count
        pending_requests_count = FriendRequest.objects.filter(
            student=request.user,
            status='PENDING'
        ).count()
        
        return render(request, 'students/home.html', {
            'pending_requests_count': pending_requests_count
        })
    except StudentProfile.DoesNotExist:
        messages.info(request, 'Please complete your profile to continue.')
        return redirect('students:profile_form')

@login_required
def mentor_requests(request):
    # Get all friend requests for this student
    friend_requests = FriendRequest.objects.filter(
        student=request.user,
        status='PENDING'
    ).select_related('instructor')
    
    return render(request, 'students/mentor_requests.html', {
        'friend_requests': friend_requests
    })

@login_required
def handle_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(
            FriendRequest, 
            id=request_id, 
            student=request.user,
            status='PENDING'
        )
        
        action = request.POST.get('action')
        if action == 'accept':
            friend_request.status = 'ACCEPTED'
            messages.success(request, f'You are now connected with {friend_request.instructor.username}')
        elif action == 'reject':
            friend_request.status = 'REJECTED'
            messages.info(request, 'Request rejected')
            
        friend_request.save()
        return redirect('students:mentor_requests')



