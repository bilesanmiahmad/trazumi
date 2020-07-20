from rest_framework import serializers
from accounts.models import User, Profile, Address


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'device_type', 'location', 'ip_address', 
            'user_type',)

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'profile')
    
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     password = validated_data.pop('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     Profile.objects.create(user=user, **profile_data)
    #     return user
    
    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     profile = instance.profile
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()

    #     profile.device_type = profile_data.get('device', profile.device_type)
    #     profile.location = profile_data.get('dob', profile.location)
    #     profile.ip_address = profile_data.get('address', profile.ip_address)
    #     profile.user_type = profile_data.get('country', profile.user_type)
    #     profile.save()

    #     return instance


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    primary_phone = serializers.IntegerField()
    secondary_phone = serializers.DecimalField(max_digits=11, decimal_places=0, allow_null=True, default=0)
    line_1 = serializers.CharField(max_length=200)
    line_2 = serializers.CharField(max_length=100, allow_blank=True, default='')
    state = serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=50)
    user_type = serializers.CharField(max_length=5)
    location = serializers.CharField(max_length=5)
    ip_address = serializers.IPAddressField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            raise serializers.ValidationError('This user already exists')
        except User.DoesNotExist:
            pass
        return value
    
    def create(self, validated_data):
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        
        primary_phone = validated_data.get('primary_phone', None)
        secondary_phone = validated_data.get('secondary_phone', None)
        user_type = validated_data.get('user_type', None)
        location = validated_data.get('location', None)
        ip_address = validated_data.get('ip_address', None)

        line_1 = validated_data.get('line_1', None)
        line_2 = validated_data.get('line_2', None)
        state = validated_data.get('state', None)
        city = validated_data.get('city', None)
        address = Address.objects.create(
            line_1=line_1,
            line_2=line_2,
            state=state,
            lga=city
        )

        profile = Profile(
            user=user, address=address, 
            primary_phone=primary_phone, 
            secondary_phone=secondary_phone, 
            user_type=user_type, location=location,
            ip_address=ip_address)
        profile.save()

        return user


        
