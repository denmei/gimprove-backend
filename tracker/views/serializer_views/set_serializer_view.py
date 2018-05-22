from rest_framework import generics
from tracker.serializers.UserProfileSerializer import *
from rest_framework.permissions import IsAuthenticated
from tracker.serializers.SetSerializer import *


# TODO: add permissions so only authenticated components can use the views.


class SetList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
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

    def delete(self, request, *args, **kwargs):
        """
        On delete, the set has to be removed from the active_set field of the user profile if it is there. Otherwise
        a foreign key error occurs.
        """
        set = Set.objects.get(id=kwargs['pk'])
        user_profile = set.exercise_unit.train_unit.user
        exercise_unit = set.exercise_unit
        train_unit = exercise_unit.train_unit
        if user_profile.active_set == set:
            user_profile.active_set = None
            user_profile.save()
        ret_val = super(SetDetail, self).destroy(request, *args, **kwargs)
        if len(Set.objects.filter(exercise_unit=exercise_unit)) == 0:
            exercise_unit.delete()
        if len(train_unit.exerciseunit_set.all()) == 0:
            train_unit.delete()
        return ret_val


class SetListByExerciseUnit(generics.ListAPIView):
    """
    View to retrieve sets by exerciseunit.
    """
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    lookup_field = 'exercise_unit'

