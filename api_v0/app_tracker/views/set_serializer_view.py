from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api_v0.app_tracker.serializers.SetSerializer import *
from app_main.models.models import UserProfile
from rest_framework import status
from rest_framework.response import Response


class SetList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Class for creating new sets or retrieving a list of sets.
    """
    serializer_class = SetSerializer

    # TODO: Limit access for creating new sets

    def get_queryset(self):
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
        if UserProfile.objects.filter(user=user).exists():
            userprofile = UserProfile.objects.get(user=user)
            userprofile_tracking = UserTrackingProfile.objects.get(user_profile=userprofile)
            trainunits = TrainUnit.objects.filter(user=userprofile_tracking)
            exerciseunits = ExerciseUnit.objects.filter(train_unit__in=trainunits)
            relevant_sets = Set.objects.filter(exercise_unit__in=exerciseunits)
            return relevant_sets.get(id=self.kwargs['pk'])
        elif Equipment.objects.filter(user=user).exists():
            equipment = Equipment.objects.get(user=user)
            relevant_sets = Set.objects.filter(equipment=equipment)
            return relevant_sets.get(id=self.kwargs['pk'])
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SetListByExerciseUnit(generics.ListAPIView):
    """
    View to retrieve sets by exerciseunit.
    """
    # TODO: Check for user
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    lookup_field = 'exercise_unit'
