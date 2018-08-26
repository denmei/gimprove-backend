from django.db.models.signals import post_save
from app_tracker.models.models import Set
from django.dispatch import receiver


@receiver(post_save, sender=Set)
def save_user_profile(sender, instance, **kwargs):
    instance.Set.save()
