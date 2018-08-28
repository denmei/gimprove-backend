from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api_v0.app_tracker.serializers.SetSerializer import *
from app_main.models.models import UserProfile


class SetList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Class for creating new sets or retrieving a list of sets.
    """
    serializer_class = SetSerializer

    # TODO: Limit access for creating new sets

    def get_queryset(self):
        # TODO: Directly filter sets for userprofile to avoid trainunit- and exerciseunit filtering!
        user = self.request.user
        userprofile = UserProfile.objects.get(user=user)
        userprofile_tracking = UserTrackingProfile.objects.get(user_profile=userprofile)
        trainunits = TrainUnit.objects.filter(user=userprofile_tracking)
        exerciseunits = ExerciseUnit.objects.filter(train_unit__in=trainunits)
        return Set.objects.filter(exercise_unit__in=exerciseunits)


class SetDetail(generics.RetrieveUpdateDestroyAPIView):
    # TODO: Check for all requests whether only the data of the user the request is coming from is changed/accessed!
    """
    View to retrieve, update or delete sets via http request.
    """
    queryset = Set.objects.all()
    serializer_class = SetSerializer

    def get_object(self):
        user = self.request.user
        userprofile = UserProfile.objects.get(user=user)
        userprofile_tracking = UserTrackingProfile.objects.get(user_profile=userprofile)
        trainunits = TrainUnit.objects.filter(user=userprofile_tracking)
        exerciseunits = ExerciseUnit.objects.filter(train_unit__in=trainunits)
        relevant_sets = Set.objects.filter(exercise_unit__in=exerciseunits)
        return relevant_sets.get(id=self.kwargs['pk'])

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
    # TODO: Check for user
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    lookup_field = 'exercise_unit'

