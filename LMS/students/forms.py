from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'email', 'phone_number', 'profile_picture', 
                 'education_level', 'skill_level', 'primary_interest', 
                 'resume', 'github_url', 'linkedin_url']
        
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input rounded-lg border-gray-300 w-full',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input rounded-lg border-gray-300 w-full',
                'placeholder': 'Enter your email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input rounded-lg border-gray-300 w-full',
                'placeholder': 'Enter your phone number'
            }),
            'education_level': forms.Select(attrs={
                'class': 'form-select rounded-lg border-gray-300 w-full'
            }),
            'skill_level': forms.RadioSelect(attrs={
                'class': 'form-radio'
            }),
            'primary_interest': forms.Select(attrs={
                'class': 'form-select rounded-lg border-gray-300 w-full'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-input rounded-lg border-gray-300 w-full',
                'placeholder': 'Your GitHub URL'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-input rounded-lg border-gray-300 w-full',
                'placeholder': 'Your LinkedIn URL'
            }),
        }