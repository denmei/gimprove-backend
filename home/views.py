from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home/homepage2.html')


def sign_up(request):
    return render(request, 'home/sign_up.html')