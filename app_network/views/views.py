
from django.contrib.auth.decorators import login_required
from app_network.models import Connection, Activity
from app_main.models.models import Profile, UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


@login_required
def create_connection(request, pk):
    connection = Connection(follower=request.user, followed=User.objects.get(id=pk))
    connection.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete_connection(request, pk):
    Connection.objects.filter(follower=request.user, followed=User.objects.get(id=pk)).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class FollowerView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'followers.html'


class ActivityListView(LoginRequiredMixin, generic.ListView):
    """
    Start page for every user.Lists activities of other users and shows current active set if available.
    """

    model = Activity
    context_object_name = 'activities'
    template_name = 'tracker/User/user_activitylist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'tracker/User/user_tracker_base.html'
        context['profile'] = UserProfile.objects.get(user=self.request.user)
        context['user_id'] = self.request.user.id
        print("user_id : " + str(self.request.user.id))
        return context
