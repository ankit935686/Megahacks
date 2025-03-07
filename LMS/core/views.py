from django.shortcuts import render

# Create your views here.

def landing_page(request):
    return render(request, 'core/home.html')

def login_options(request):
    return render(request, 'core/login_options.html')
