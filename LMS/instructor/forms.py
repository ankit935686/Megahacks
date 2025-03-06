from django import forms
from .models import InstructorProfile

class InstructorProfileForm(forms.ModelForm):
    expertise = forms.MultipleChoiceField(
        choices=InstructorProfile.EXPERTISE_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = InstructorProfile
        fields = [
            'full_name', 'profile_picture', 'contact_number','resume',
            'expertise', 'years_of_experience', 'linkedin_profile', 'bio'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 