from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('generate-roadmap/<int:resume_id>/', views.generate_roadmap, name='generate_roadmap'),
    path('view-roadmap/<int:roadmap_id>/', views.view_roadmap, name='view_roadmap'),
] 