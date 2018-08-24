from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api_v0.main.serializers.UserProfileSerializer import UserProfileSerializer
from main.models.models import UserProfile


class UserProfileDetail(generics.RetrieveAPIView):
    """
    View to retrieve UserProfileData via http request and by User_id.
    """
    serializer_class = UserProfileSerializer

    def delete(self, request, *args, **kwargs):
        """
        On delete, the set has to be removed from the active_set field of the user profile if it is there. Otherwise
        a foreign key error occurs.
        """
        profile = UserProfile.objects.get(user=self.request.user)
        user = profile.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user=user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(user=self.request.user)
        return obj


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
