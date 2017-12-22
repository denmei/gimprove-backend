from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/tracker/')
    else:
        return render(request, 'home/homepage2.html')


def sign_up(request):
    return render(request, 'home/sign_up.html')