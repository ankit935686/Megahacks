from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    output = models.TextField(blank=True)
    error = models.TextField(blank=True)
    execution_time = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s submission - {self.created_at}"

class Room(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(User, related_name='player1_rooms', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2_rooms', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Room {self.room_id}"

class CodingQuestion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    test_cases = models.JSONField()
    function_name = models.CharField(max_length=100, null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.difficulty})"

class Battle(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE)
    player1_code = models.TextField(blank=True)
    player2_code = models.TextField(blank=True)
    player1_completed = models.BooleanField(default=False)
    player2_completed = models.BooleanField(default=False)
    player1_results = models.JSONField(default=list)
    player2_results = models.JSONField(default=list)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
