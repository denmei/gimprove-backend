from django.db import models
from django.contrib.auth.models import User
from app_main.models.models import get_image_path


class Achievement(models.Model):
    name = models.CharField(max_length=100, help_text="Insert the name of the achievement here.", primary_key=True)
    description = models.TextField(max_length=500, help_text="What did the user do to achieve it?", null=True,
                                   blank=True)
    user = models.ManyToManyField(User, blank=True)
    achievement_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return str(self.name)
