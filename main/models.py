from django.db import models
import os
from django.utils import timezone
from django.contrib.auth.models import User


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.pk), filename)


class Profile(models.Model):
    """
    Abstract class for the two user types - gyms and athletes (users). Attributes:
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True, help_text="Beschreibung.")
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    """
    def get_follows_connections(self):
        connections = Connection.objects.filter(follower=self.user)
        return connections

    def get_follower_connections(self):
        connections = Connection.objects.filter(followed=self.user)
        return connections

    def get_follow_ids(self):
        
        :return: List of the ids of the Users the Profile is following.
        
        connections = Connection.objects.filter(follower=self.user)
        follows = connections.values_list('followed', flat=True)
        return follows

    def get_activities(self):
        activities = Activity.objects.filter(user=self.user)
        return activities

    def get_follows_activities(self):
        activities = Activity.objects.filter().order_by('-created')
        return activities
    """

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.user)


class UserProfile(Profile):
    """
    Extended Profile for personal users (not Gyms).
    """
    date_of_birth = models.DateField(null=False, blank=False)
    gym = models.ManyToManyField('GymProfile', blank=True)
    rfid_tag = models.CharField('RFID', max_length=10, blank=True, null=True)
    # achievements = models.ManyToManyField('Achievement', blank=True)
    _pr_active_set = models.ForeignKey('Set', blank=True, null=True, on_delete=models.DO_NOTHING)

    @property
    def active_set(self):
        """
        Returns active set. If set has not been changed during the last 15 seconds, returns None.
        """
        if self._pr_active_set is not None:
            time_diff = timezone.now() - self._pr_active_set.last_update
            if time_diff.seconds > 15:
                self._pr_active_set = None
        return self._pr_active_set

    @active_set.setter
    def active_set(self, a_set):
        self._pr_active_set = a_set


class GymProfile(Profile):
    """
    Extended Profile for gym users.
    """
    members = models.ManyToManyField('UserProfile', blank=True)
