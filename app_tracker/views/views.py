#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView
from app_tracker.models.models import *

from app_tracker.forms.forms import AddExerciseUnitForm, AddTrainUnitForm


def set(request, pk):
    return None


class TrainingUnitsList(LoginRequiredMixin, generic.ListView):
    """
    Show all training units of a user.
    """
    model = TrainUnit
    context_object_name = 'training_units'
    template_name = 'tracker/User/training_units.html'

    def get_context_data(self, **kwargs):
        """
        Set base template and context.
        """
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'tracker/User/user_tracker_base.html'
        return context

    def get_queryset(self):
        """
        Show only training units of the current user.
        """
        return TrainUnit.objects.filter(user=self.request.user.userprofile)


class ExerciseUnitList(LoginRequiredMixin, generic.ListView):
    """
    Show all exercise units of a particular training unit.
    """
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


class AddExerciseUnit(LoginRequiredMixin, CreateView):
    """
    Adding a exercise unit to a train unit.
    """
    model = ExerciseUnit
    form_class = AddExerciseUnitForm

    def get_initial(self):
        return {'train_unit': self.kwargs.get('pk'), 'time_date': datetime.datetime.today()}

    def get_success_url(self):
        return reverse('exercise_unit_list', args=[str(self.kwargs.get('pk'))])


class DeleteTrainingUnit(LoginRequiredMixin, DeleteView):
    """
    Delete a complete training unit with all related exercise units.
    """
    model = TrainUnit
    success_url = reverse_lazy('training_units')
    context_object_name = 'training_unit'


class AddTrainingUnit(LoginRequiredMixin, CreateView):
    """
    Add new training unit.
    """
    model = TrainUnit
    context_object_name = 'training_unit'
    template_name = "add_train_unit.html"
    form_class = AddTrainUnitForm
    success_url = reverse_lazy('training_units')

    def get_initial(self):
        return {'date': datetime.date.today(), 'user': self.request.user, 'start_time_date': datetime.datetime.today(),
                'end_time_date': datetime.datetime.today()}
