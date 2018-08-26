from app_main.models.models import GymProfile, UserProfile, get_profile_type
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    """
    Show profile of user.
    """
    model = UserProfile
    context_object_name = 'profile'
    template_name = 'tracker/User/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'tracker/User/user_tracker_base.html'
        return context


class GymView(LoginRequiredMixin, generic.DetailView):
    model = GymProfile
    context_object_name = 'gym'
    template_name = 'gym.html'
