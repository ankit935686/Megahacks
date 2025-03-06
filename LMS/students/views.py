from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    return render(request, 'students/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('students:home')
    else:
        form = UserCreationForm()
    return render(request, 'students/signup.html', {'form': form})

@login_required
def home(request):
    return render(request, 'students/home.html')
