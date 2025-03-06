from django.contrib import admin
from .models import StudentResume, CareerRoadmap

@admin.register(StudentResume)
class StudentResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username', 'resume_text')
    date_hierarchy = 'uploaded_at'

@admin.register(CareerRoadmap)
class CareerRoadmapAdmin(admin.ModelAdmin):
    list_display = ('user', 'generated_at')
    list_filter = ('generated_at',)
    search_fields = ('user__username', 'roadmap_content', 'suggestions')
    date_hierarchy = 'generated_at'
    readonly_fields = ('generated_at',)
