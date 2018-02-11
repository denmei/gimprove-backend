from tracker.serializers import *
from rest_framework import generics


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
    View to retrieve UserProfileData via http request.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

