from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class MentorshipSlot(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.instructor.username} - {self.date} ({self.start_time}-{self.end_time})"

class MentorshipSession(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_sessions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_sessions')
    slot = models.ForeignKey(MentorshipSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    meet_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"Session: {self.instructor.username} with {self.student.username}"

class InstructorProfile(models.Model):
    EXPERTISE_CHOICES = [
        ('AI', 'Artificial Intelligence'),
        ('WEB', 'Web Development'),
        ('DATA', 'Data Science'),
        ('MOBILE', 'Mobile Development'),
        ('CLOUD', 'Cloud Computing'),
        ('DEVOPS', 'DevOps'),
        ('SECURITY', 'Cybersecurity'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='instructor_profiles/', null=True, blank=True)
    resume = models.FileField(upload_to='instructor_resumes/', null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    expertise = models.JSONField(help_text="Store multiple expertise areas")
    years_of_experience = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    linkedin_profile = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name}'s Profile"

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    
    instructor = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['instructor', 'student']
