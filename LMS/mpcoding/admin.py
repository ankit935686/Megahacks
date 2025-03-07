from django.contrib import admin
from .models import CodeSubmission

@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('user__username', 'code')
