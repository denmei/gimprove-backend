from django.shortcuts import render
from django.views import generic
from .models import TrainUnit
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
    """View function for home page of site."""
    return render(request, 'index.html')


class TrainingUnitsList(LoginRequiredMixin, generic.ListView):
    model = TrainUnit
    context_object_name = 'training_units_list'
    template_name = 'training_units.html'

    def get_queryset(self):
        return TrainUnit.objects.filter(user=self.request.user)
