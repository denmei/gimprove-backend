from rest_framework import generics
from tracker.serializers.UserProfileSerializer import *

# TODO: add permissions so only authenticated components can use the views.


class UserProfileDetail(generics.RetrieveAPIView):
    """
    View to retrieve UserProfileData via http request and by User_id.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailByRfid(generics.RetrieveAPIView):
    """
    View to retrieve UserProfileData via http request and by UserProfile_RFID.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'rfid_tag'
