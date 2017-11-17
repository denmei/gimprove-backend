from django.shortcuts import render
from django.views import generic
from .models import TrainUnit, Profile, ExerciseUnit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
import datetime
from .forms import AddExerciseUnitForm, AddTrainUnitForm
from django.views.generic.edit import CreateView, DeleteView

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


class ExerciseUnitList(LoginRequiredMixin, generic.ListView):
    model = ExerciseUnit
    context_object_name = 'exercise_unit_list'
    template_name = 'exercise_unit_list.html'

    def get_queryset(self):
        train_unit = get_object_or_404(TrainUnit, pk=self.kwargs['pk'])
        return ExerciseUnit.objects.filter(train_unit=train_unit)

    def get_context_data(self, **kwargs):
        context = super(ExerciseUnitList, self).get_context_data(**kwargs)
        context['training_unit'] = get_object_or_404(TrainUnit, pk=self.kwargs['pk'])
        return context


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile.html'


class AddExerciseUnit(CreateView):
    model = ExerciseUnit
    form_class = AddExerciseUnitForm
    success_url = reverse_lazy('training_units')

    def get_initial(self):
        return {'train_unit': self.kwargs.get('pk'), 'time_date': datetime.datetime.today()}


class DeleteTrainingUnit(DeleteView):
    model = TrainUnit
    success_url = reverse_lazy('training_units')
    context_object_name = 'training_unit'


class AddTrainingUnit(CreateView):
    model = TrainUnit
    context_object_name = 'training_unit'
    template_name = "add_train_unit.html"
    form_class = AddTrainUnitForm
    success_url = reverse_lazy('training_units')

    def get_initial(self):
        return {'date': datetime.date.today(), 'user': self.request.user, 'start_time_date': datetime.datetime.today(),
                'end_time_date': datetime.datetime.today()}
