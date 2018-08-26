from django.db import models
from django.contrib.auth.models import User
import uuid


class Connection(models.Model):
    """
    Connection between a follower and the followed profile.
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.follower) + ":" + str(self.followed)


class Activity(models.Model):
    """
    New training units, achievements etc.create activities that can be shared in the community.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(max_length=500, help_text="What kind of activity?", null=True,
                                   blank=True)

    def __str__(self):
        return str(self.user) + ": " + str(self.created)
