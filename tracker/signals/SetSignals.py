from django.db.models.signals import post_delete, pre_init
from django.dispatch import receiver
from tracker.models.models import Set, ExerciseUnit


@receiver(post_delete, sender=Set)
def delete_empty_exercise_units(sender, instance, created, **kwargs):
    print("DELETE SET")
    print(sender)
    print(instance)


@receiver(pre_init, sender=Set)
def create_exercise_unit(sender, args, **kwargs):
    pass


@receiver(pre_init, sender=ExerciseUnit)
def create_train_unit(sender, args, **kwargs):
    pass


@receiver(post_delete, sender=ExerciseUnit)
def delete_empty_train_units(sender, instance, created, **kwargs):
    pass
