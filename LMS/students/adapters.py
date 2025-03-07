from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse
from .models import StudentProfile

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        try:
            profile = request.user.studentprofile
            if not profile.is_profile_completed:
                return reverse('students:profile_form')
        except StudentProfile.DoesNotExist:
            return reverse('students:profile_form')
        return reverse('students:home')

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        return reverse('students:profile_form')

    def get_login_redirect_url(self, request):
        try:
            profile = request.user.studentprofile
            if not profile.is_profile_completed:
                return reverse('students:profile_form')
        except StudentProfile.DoesNotExist:
            return reverse('students:profile_form')
        return reverse('students:home')

    def pre_social_login(self, request, sociallogin):
        super().pre_social_login(request, sociallogin)
        if sociallogin.is_existing:
            try:
                user = sociallogin.user
                profile = StudentProfile.objects.get(user=user)
                if not profile.is_profile_completed:
                    request.session['redirect_to_profile'] = True
            except StudentProfile.DoesNotExist:
                request.session['redirect_to_profile'] = True