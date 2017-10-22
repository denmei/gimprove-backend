from django.shortcuts import render
from django.views import generic
from .models import TrainUnit, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    """View function for home page of site."""
    return render(request, 'index.html')


class TrainingUnitsList(LoginRequiredMixin, generic.ListView):
    model = TrainUnit
    context_object_name = 'training_units_list'
    template_name = 'training_units.html'


class TrainingUnitDetail(LoginRequiredMixin, generic.DetailView):
    model = TrainUnit
    context_object_name = 'training_unit'
    template_name = 'train_unit.html'


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile.html'
