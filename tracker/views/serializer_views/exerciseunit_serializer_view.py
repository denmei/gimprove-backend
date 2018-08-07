from rest_framework import generics
from tracker.serializers.ExerciseUnitSerializer import *
from rest_framework.permissions import IsAuthenticated


class ExerciseUnitList(generics.ListAPIView):
    """
    Class for creating new sets or retrieving a list of sets.
    """
    serializer_class = ExerciseUnitSerializer

    def get_queryset(self):
        user = self.request.user
        userprofile = UserProfile.objects.get(user=user)
        trainunits = TrainUnit.objects.filter(user=userprofile)
        exerciseunits = ExerciseUnit.objects.filter(train_unit__in=trainunits)
        return exerciseunits


class ExerciseUnitDetail(generics.RetrieveDestroyAPIView):
    """
    View to retrieve or delete ExerciseUnits via http request.
    """
    queryset = ExerciseUnit.objects.all()
    serializer_class = ExerciseUnitSerializer


class ExerciseUnitListByTrainUnit(generics.ListAPIView):
    """
    View to retrieve ExerciseUnits by TrainUnit.
    """
    queryset = ExerciseUnit.objects.all()
    serializer_class = ExerciseUnitSerializer
    lookup_field = 'train_unit'
