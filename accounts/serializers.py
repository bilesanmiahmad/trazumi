from rest_framework import serializers
from accounts.models import User, Profile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'device_type', 'location', 'ip_address', 
            'user_type',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = (
            'url', 'email', 'first_name', 'last_name',
            'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.device_type = profile_data.get('device', profile.device_type)
        profile.location = profile_data.get('dob', profile.location)
        profile.ip_address = profile_data.get('address', profile.ip_address)
        profile.user_type = profile_data.get('country', profile.user_type)
        profile.save()

        return instance