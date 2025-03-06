from django.contrib import admin
from .models import MentorshipSlot, MentorshipSession

# Register your models here.
admin.site.register(MentorshipSlot)
admin.site.register(MentorshipSession)
