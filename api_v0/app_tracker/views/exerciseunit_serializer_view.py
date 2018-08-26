from rest_framework import generics
from api_v0.app_tracker.serializers.ExerciseUnitSerializer import ExerciseUnitSerializer
from app_tracker.models.models import UserTrackingProfile, TrainUnit, ExerciseUnit
from app_main.models.models import UserProfile


class ExerciseUnitList(generics.ListAPIView):
    """
    Class for creating new sets or retrieving a list of sets.
    """
    serializer_class = ExerciseUnitSerializer

    def get_queryset(self):
        user = self.request.user
        userprofile = UserProfile.objects.get(user=user)
        user_tracking_profile = UserTrackingProfile.objects.get(user_profile=userprofile)
        trainunits = TrainUnit.objects.filter(user=user_tracking_profile)
        exerciseunits = ExerciseUnit.objects.filter(train_unit__in=trainunits)
        return exerciseunits


class ExerciseUnitDetail(generics.RetrieveDestroyAPIView):
    """
    View to retrieve or delete ExerciseUnits via http request.
    """
    # TODO: Check for user
    queryset = ExerciseUnit.objects.all()
    serializer_class = ExerciseUnitSerializer


class ExerciseUnitListByTrainUnit(generics.ListAPIView):
    """
    View to retrieve ExerciseUnits by TrainUnit.
    """
    # TODO: Check for user
    queryset = ExerciseUnit.objects.all()
    serializer_class = ExerciseUnitSerializer
    lookup_field = 'train_unit'
