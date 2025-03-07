from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect

class StudentProfile(models.Model):
    EDUCATION_CHOICES = [
        ('high_school', 'High School'),
        ('bachelors', "Bachelor's Degree"),
        ('masters', "Master's Degree"),
        ('phd', 'Ph.D.'),
        ('other', 'Other'),
    ]
    
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    INTEREST_CHOICES = [
        ('web_dev', 'Web Development'),
        ('mobile_dev', 'Mobile Development'),
        ('data_science', 'Data Science'),
        ('devops', 'DevOps'),
        ('ai_ml', 'AI/Machine Learning'),
        ('cybersecurity', 'Cybersecurity'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    primary_interest = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    resume = models.FileField(upload_to='resumes/', blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=SocialAccount)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.get_or_create(
            user=instance.user,
            defaults={
                'email': instance.user.email or '',
                'full_name': instance.user.get_full_name() or instance.user.username
            }
        )
