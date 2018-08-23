from rest_framework import generics
from tracker.api_v0.serializers.ExerciseUnitSerializer import ExerciseUnitSerializer
from tracker.models.models import UserTrackingProfile, TrainUnit, ExerciseUnit


class ExerciseUnitList(generics.ListAPIView):
    """
    Class for creating new sets or retrieving a list of sets.
    """
    serializer_class = ExerciseUnitSerializer

    def get_queryset(self):
        user = self.request.user
        userprofile = UserTrackingProfile.objects.get(user=user)
        trainunits = TrainUnit.objects.filter(user=userprofile)
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
