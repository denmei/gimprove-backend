from rest_framework import serializers

from tracker.main.models.models import *


# TODO: Add permission to restrict access only to authenticated equipment components


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfiles.

    Allows to retrieve User Data.
    """
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)
    username = serializers.CharField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'date_of_birth', 'gym', 'rfid_tag', 'achievements', 'active_set', 'bio', 'profile_image',
                  'username')

    def create(self, validated_data, **kwargs):
        """
        Remove additional parameters (rfid and exercise name) before creating the set-instance.
        """
        achievements = validated_data.pop("achievements")
        gyms = validated_data.pop("gym")
        name = validated_data.pop("username")

        new_user = User.objects.create_user(username=name)
        validated_data.update({'user': new_user})
        new_profile = UserProfile.objects.create(**validated_data)

        # add gyms if available
        for gym in gyms:
            new_profile.gym.add(gym)

        new_profile.save()
        return new_profile
