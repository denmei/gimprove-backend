from django.shortcuts import render
from app_achievements.models.models import Achievement
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class AchievementView(LoginRequiredMixin, generic.ListView):
    model = Achievement
    context_object_name = 'achievements'
    template_name = 'achievements.html'
