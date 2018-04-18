from rest_framework import generics
from tracker.serializers.UserProfileSerializer import *
from tracker.serializers.ExerciseUnitSerializer import *


# TODO: add permissions so only authenticated components can use the views.


class ExerciseUnitList(generics.ListCreateAPIView):
    """
    Class for creating new sets or retrieving a list of sets.
    """
    queryset = Set.objects.all()
    serializer_class = ExerciseUnitSerializer


class ExerciseUnitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete ExerciseUnits via http request.
    """
    queryset = ExerciseUnit.objects.all()
    serializer_class = ExerciseUnitSerializer
