from rest_framework import serializers
from profiles.models import Profile, ProfileStatus


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    avater = serializers.ImageField(read_only=True) # ProfileSerializerを使うビューではupdateできなくする。

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileAvaterSerializer(serializers.ModelSerializer):
   
   class Meta:
       model = Profile
       fields = ("avater",) # avaterのみアクセスできる。データの変更などはこのシリアライザーを使わないとできない。


class ProfileStatusSerialzier(serializers.ModelSerializer):

    user_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileStatus
        fields = "__all__"