from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a profile"""
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(allow_blank=True, required=False,
                                       min_length=2, max_length=50)
    last_name = serializers.CharField(allow_blank=True, required=False,
                                      min_length=2, max_length=50)
    bio = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ('email', 'bio', 'image', 'first_name', 'last_name')
