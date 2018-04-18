from rest_framework import generics
from tracker.serializers.ExerciseUnitSerializer import *


class ExerciseUnitList(generics.ListAPIView):
    """
    Class for creating new sets or retrieving a list of sets.
    """
    queryset = ExerciseUnit.objects.all()
    serializer_class = ExerciseUnitSerializer


class ExerciseUnitDetail(generics.RetrieveDestroyAPIView):
    """
    View to retrieve, update or delete ExerciseUnits via http request.
    """
    queryset = ExerciseUnit.objects.all()
    serializer_class = ExerciseUnitSerializer
