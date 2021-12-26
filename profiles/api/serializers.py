from rest_framework import serializers
from profiles.models import Profiles, ProfileStatus


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    avater = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileAvaterSerializer(serializers.ModelSerializer):
   
   class Meta:
       model = Profile
       fields = ("avater",)


class ProfileStatusSerialzier(serializers.ModelSerializer):

    user_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileStatus
        fields = "__all__"