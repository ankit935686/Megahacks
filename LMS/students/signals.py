from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login, social_account_added
from .models import StudentProfile

@receiver(user_signed_up)
def user_signed_up_signal(request, user, **kwargs):
    """Create a user profile when a new user signs up"""
    # Check if the registration is coming from instructor paths
    if request and (request.path.startswith('/instructor/') or 'instructor' in request.GET.get('next', '')):
        return  # Don't create StudentProfile for instructors
        
    StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'email': user.email or '',
            'full_name': user.get_full_name() or user.username
        }
    )

@receiver(pre_social_login)
def pre_social_login_signal(request, sociallogin, **kwargs):
    """Check if user needs to complete profile on social login"""
    # Check if this is an instructor login
    if request and request.path.startswith('/instructor/'):
        return  # Don't handle student profile for instructors
        
    if sociallogin.is_existing:
        try:
            user = sociallogin.user
            profile = StudentProfile.objects.get(user=user)
            if not profile.is_profile_completed:
                request.session['redirect_to_profile'] = True
        except StudentProfile.DoesNotExist:
            request.session['redirect_to_profile'] = True

@receiver(social_account_added)
def social_account_added_signal(request, sociallogin, **kwargs):
    """Handle new social account connections"""
    # Check if this is an instructor
    if request and request.path.startswith('/instructor/'):
        return  # Don't handle student profile for instructors
        
    user = sociallogin.user
    profile, created = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'email': user.email or '',
            'full_name': user.get_full_name() or user.username
        }
    )
    if not profile.is_profile_completed:
        request.session['redirect_to_profile'] = True