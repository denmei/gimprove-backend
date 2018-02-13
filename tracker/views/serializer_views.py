from tracker.serializers import *
from rest_framework import generics

"""
These views may only be used by authenticated components.
"""

# TODO: add permissions so only authenticated components can use the views.


class SetList(generics.ListCreateAPIView):
    """
    Class for creating new sets or retrieving a list of sets.
    """
    queryset = Set.objects.all()
    serializer_class = SetSerializer


class SetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete sets via http request.
    """
    queryset = Set.objects.all()
    serializer_class = SetSerializer


class UserProfileDetail(generics.RetrieveAPIView):
    """
    View to retrieve UserProfileData via http request and by User_id.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

"""
class UserProfileDetailByRfid(generics.RetrieveAPIView):

    View to retrieve UserProfileData via http request and by UserProfile_RFID.

    # TODO: By RFID. Add URL
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
"""