import json
from rest_framework import serializers
from tracker.models.models import *

# TODO: Add permission to restrict access only to authenticated equipment components


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfiles.

    Allows to retrieve User Data.
    """
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = (['user', 'rfid_tag', 'active_set'])