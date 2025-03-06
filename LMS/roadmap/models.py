from django.db import models
from django.contrib.auth.models import User

class StudentResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CareerRoadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(StudentResume, on_delete=models.CASCADE)
    roadmap_content = models.TextField()
    suggestions = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Roadmap for {self.user.username} - {self.generated_at.date()}"
