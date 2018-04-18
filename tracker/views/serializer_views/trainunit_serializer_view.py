from rest_framework import generics
from tracker.serializers.TrainUnitSerializer import *


class TrainUnitList(generics.ListAPIView):
    """
    Class for retrieving a list of trainunits.
    """
    queryset = TrainUnit.objects.all()
    serializer_class = TrainUnitSerializer


class TrainUnitDetail(generics.RetrieveDestroyAPIView):
    """
    Class for retrieving or deleting a single trainunit.
    """
    queryset = TrainUnit.objects.all()
    serializer_class = TrainUnitSerializer
