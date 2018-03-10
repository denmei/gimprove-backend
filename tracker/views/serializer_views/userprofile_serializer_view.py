from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from tracker.serializers.UserProfileSerializer import *


# TODO: add permissions so only authenticated components can use the views


class UserProfileDetail(generics.RetrieveAPIView):
    """
    View to retrieve UserProfileData via http request and by User_id.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def delete(self, request, *args, **kwargs):
        """
        On delete, the set has to be removed from the active_set field of the user profile if it is there. Otherwise
        a foreign key error occurs.
        """
        profile = UserProfile.objects.get(user_id=kwargs['pk'])
        user = profile.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileDetailByRfid(generics.RetrieveAPIView):
    """
    View to retrieve UserProfileData via http request and by UserProfile_RFID.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'rfid_tag'


class UserProfileCreator(generics.CreateAPIView):
    """
    View to create a new UserProfile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
