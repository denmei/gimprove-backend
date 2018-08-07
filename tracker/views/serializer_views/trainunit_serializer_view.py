from rest_framework import generics
from tracker.serializers.TrainUnitSerializer import *
from rest_framework.permissions import IsAuthenticated


class TrainUnitList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Class for retrieving a list of trainunits.
    """
    serializer_class = TrainUnitSerializer

    def get_queryset(self):
        user = self.request.user
        userprofile = UserProfile.objects.get(user=user)
        trainunits = TrainUnit.objects.filter(user=userprofile)
        return trainunits


class TrainUnitDetail(generics.RetrieveDestroyAPIView):
    """
    Class for retrieving or deleting a single trainunit.
    """
    queryset = TrainUnit.objects.all()
    serializer_class = TrainUnitSerializer


class TrainUnitListByUserId(generics.ListAPIView):
    """
    View to retrieve a user's trainunits by the user id.
    """
    queryset = TrainUnit.objects.all()
    serializer_class = TrainUnitSerializer
    lookup_field = 'user'
