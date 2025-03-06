from django.contrib import admin
from .models import MentorshipSlot, MentorshipSession, InstructorProfile

# Register your models here.
admin.site.register(MentorshipSlot)
admin.site.register(MentorshipSession)
admin.site.register(InstructorProfile)
