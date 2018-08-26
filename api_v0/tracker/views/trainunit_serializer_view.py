from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api_v0.tracker.serializers.TrainUnitSerializer import TrainUnitSerializer
from app_tracker.models.models import UserTrackingProfile, TrainUnit


class TrainUnitList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Class for retrieving a list of trainunits.
    """
    serializer_class = TrainUnitSerializer

    def get_queryset(self):
        user = self.request.user
        userprofile = UserTrackingProfile.objects.get(user=user)
        trainunits = TrainUnit.objects.filter(user=userprofile)
        return trainunits


class TrainUnitDetail(generics.RetrieveDestroyAPIView):
    """
    Class for retrieving or deleting a single trainunit.
    """
    # TODO: Check for user
    queryset = TrainUnit.objects.all()
    serializer_class = TrainUnitSerializer


class TrainUnitListByUserId(generics.ListAPIView):
    """
    View to retrieve a user's trainunits by the user id.
    """
    # TODO: Check for user
    queryset = TrainUnit.objects.all()
    serializer_class = TrainUnitSerializer
    lookup_field = 'user'
