from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import MentorshipSlot, MentorshipSession, InstructorProfile, FriendRequest
from datetime import datetime, timedelta
from .forms import InstructorProfileForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse




# Create your views here.



@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('instructor:login')
    
    # Only check for profile if user is authenticated
    if not hasattr(request.user, 'instructorprofile'):
        return redirect('instructor:create_profile')
    return render(request, 'home.html')
    


def login_view(request):
    if request.user.is_authenticated:
        return redirect('instructor:home')
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('instructor:home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('instructor:home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def mentorship_dashboard(request):
    upcoming_sessions = MentorshipSession.objects.filter(
        instructor=request.user,
        status='APPROVED',
        slot__date__gte=datetime.now().date()
    ).order_by('slot__date', 'slot__start_time')
    
    pending_requests = MentorshipSession.objects.filter(
        instructor=request.user,
        status='PENDING'
    ).order_by('slot__date')
    
    context = {
        'upcoming_sessions': upcoming_sessions,
        'pending_requests': pending_requests,
    }
    return render(request, 'instructor/mentorship/dashboard.html', context)

@login_required
def manage_slots(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        MentorshipSlot.objects.create(
            instructor=request.user,
            date=date,
            start_time=start_time,
            end_time=end_time
        )
        messages.success(request, 'Slot added successfully!')
        return redirect('instructor:manage_slots')
    
    available_slots = MentorshipSlot.objects.filter(
        instructor=request.user,
        date__gte=datetime.now().date(),
        is_available=True
    ).order_by('date', 'start_time')
    
    return render(request, 'instructor/mentorship/manage_slots.html', {'slots': available_slots})

@login_required
def manage_sessions(request):
    sessions = MentorshipSession.objects.filter(
        instructor=request.user
    ).order_by('-created_at')
    return render(request, 'instructor/mentorship/sessions.html', {'sessions': sessions})

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(MentorshipSession, id=session_id, instructor=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            session.status = 'APPROVED'
            session.meet_link = request.POST.get('meet_link')
        elif action == 'reject':
            session.status = 'REJECTED'
        elif action == 'complete':
            session.status = 'COMPLETED'
            session.feedback = request.POST.get('feedback')
            session.rating = request.POST.get('rating')
        
        session.save()
        messages.success(request, f'Session {action}d successfully!')
        return redirect('instructor:mentorship_dashboard')
    
    return render(request, 'instructor/mentorship/session_detail.html', {'session': session})

@login_required
def create_profile(request):
    # Check if profile already exists
    try:
        profile = request.user.instructorprofile
        return redirect('instructor:home')
    except InstructorProfile.DoesNotExist:
        if request.method == 'POST':
            form = InstructorProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Profile created successfully!')
                return redirect('instructor:home')
        else:
            form = InstructorProfileForm(initial={'email': request.user.email})
        
        return render(request, 'instructor/create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    profile = get_object_or_404(InstructorProfile, user=request.user)
    
    if request.method == 'POST':
        form = InstructorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('instructor:home')
    else:
        form = InstructorProfileForm(instance=profile)
    
    return render(request, 'instructor/edit_profile.html', {'form': form})

@login_required
def student_list(request):
    # Get all students with completed profiles
    students = User.objects.filter(
        studentprofile__isnull=False,
        studentprofile__is_profile_completed=True
    ).exclude(id=request.user.id).select_related('studentprofile')
    
    # Get friend request status for each student
    for student in students:
        friend_request = FriendRequest.objects.filter(
            instructor=request.user,
            student=student
        ).first()
        student.friend_request_status = friend_request.status if friend_request else None
    
    return render(request, 'instructor/mentorship/student_list.html', {
        'students': students
    })

@login_required
def send_friend_request(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(User, id=student_id)
        FriendRequest.objects.get_or_create(
            instructor=request.user,
            student=student,
            defaults={'status': 'PENDING'}
        )
        messages.success(request, f'Friend request sent to {student.username}')
    return redirect('instructor:student_list')

@login_required
def my_students(request):
    # Get all accepted friend requests
    accepted_requests = FriendRequest.objects.filter(
        instructor=request.user,
        status='ACCEPTED'
    )
    students = [req.student for req in accepted_requests]
    return render(request, 'instructor/mentorship/my_students.html', {
        'students': students
    })


