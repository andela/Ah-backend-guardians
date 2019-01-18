from rest_framework import serializers
from authors.apps.core.validation import ValidateRegistrationData

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing a profile
    """
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(allow_blank=True, required=False,
                                       min_length=2, max_length=50)
    last_name = serializers.CharField(allow_blank=True, required=False,
                                      min_length=2, max_length=50)
    bio = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ('email', 'bio', 'image', 'first_name', 'last_name')


class EditProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for editing a profile
    """
    first_name = serializers.CharField(allow_blank=True, required=False,
                                       min_length=2, max_length=50)
    last_name = serializers.CharField(allow_blank=True, required=False,
                                      min_length=2, max_length=50)
    bio = serializers.CharField(allow_blank=True, required=False)

    def validate(self, data):
        """
        Function to validate how the data format is inserted
        """

        invalid_data_sent = data.get('bio') is None \
            and data.get('image') is None and data.get("first_name") is None \
            and data.get("last_name") is None

        if invalid_data_sent:
            raise serializers.ValidationError(
                'Please enter the data correctly.'
            )
        return data

    class Meta:
        model = Profile
        fields = ('bio', 'image', 'first_name', 'last_name')
