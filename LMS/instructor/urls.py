from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name='home'),
     path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('mentorship/', views.mentorship_dashboard, name='mentorship_dashboard'),
    path('mentorship/slots/', views.manage_slots, name='manage_slots'),
    path('mentorship/sessions/', views.manage_sessions, name='manage_sessions'),
    path('mentorship/session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]

