from django.db import models
from django.contrib.auth.models import User

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
