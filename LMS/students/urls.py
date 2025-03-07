from django.urls import path
from . import views


app_name = 'students'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_form, name='profile_form'),
    
    
    
    
   
    
] 