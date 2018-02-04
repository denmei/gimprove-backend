from django.shortcuts import render
from django.views import generic
from .models import *
from .serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import AddExerciseUnitForm, AddTrainUnitForm, ContactForm
from django.views.generic.edit import CreateView, DeleteView
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status


def index(request):
    if get_profile_type(request.user) == 'gym':
        return render(request, 'tracker/Gym/gym_tracker_base.html')
    return redirect('activities', request.user.id)


def about(request):
    return render(request, 'about.html')


def create_connection(request, pk):
    connection = Connection(follower=request.user, followed=User.objects.get(id=pk))
    connection.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_connection(request, pk):
    Connection.objects.filter(follower=request.user, followed=User.objects.get(id=pk)).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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


class AchievementView(LoginRequiredMixin, generic.ListView):
    model = Achievement
    context_object_name = 'achievements'
    template_name = 'achievements.html'


class GymView(LoginRequiredMixin, generic.DetailView):
    model = GymProfile
    context_object_name = 'gym'
    template_name = 'gym.html'


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


class FollowerView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'followers.html'


class ActivityListView(LoginRequiredMixin, generic.ListView):
    model = Activity
    context_object_name = 'activities'
    template_name = 'tracker/User/user_activitylist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'tracker/User/user_tracker_base.html'
        return context


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('subscription_email_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" + '',
                ['meisnerdennis@web.de'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            return redirect('contact')

    return render(request, 'contact.html', {
        'form': form_class
    })


"""class SetList(generics.ListCreateAPIView):
    queryset = Set.objects.all()
    serializer_class = SetSerializer"""


class SetList(generics.ListCreateAPIView):
    """
    Class for creating new sets or retrieving a list of sets.
    """
    queryset = Set.objects.all()
    serializer_class = SetSerializer


class SetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete sets via http request.
    """
    queryset = Set.objects.all()
    serializer_class = SetSerializer
