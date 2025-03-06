from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



# Create your views here.



@login_required
def home(request):
    return render(request, 'home.html')


def login_view(request):
    return render(request, 'instructor/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('instructor:home')
    else:
        form = UserCreationForm()
    return render(request, 'instructor/signup.html', {'form': form})


