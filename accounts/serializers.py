from rest_framework import serializers
from .models import User, Profile, Address


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile.objects.create(user=user)
        return user
    
    def validate_email(self, value):
        val_email = value.lower()
        try:
            User.objects.get(email=val_email)
            return serializers.ValidationError('User already exists')
        except User.DoesNotExist:
            return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'verification_pin']


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['line_1', 'line_2', 'town', 'city', 'state', 'lga']


class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'device_type', 'ip_address', 'location', 'user_type', 'primary_phone', 'address']


class FullUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'verification_pin', 'auth_token', 'profile']


class ActivateUserSerilaizer(serializers.Serializer):
    email = serializers.EmailField()
    pin = serializers.IntegerField()

    def validate(self, data):
        email = data.get('email', None)
        pin = data.get('pin', None)
        try:
            user = User.objects.get(email=email, verification_pin=pin)
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError('Email or verification key is wrong')
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email', None)
        try:
            user = User.objects.get(email=email)
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError('User with email does not exist')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if len(password) < 8:
            raise serializers.ValidationError('Password should be 8 or more characters')
        elif password != confirm_password:
            raise serializers.ValidationError('Passwords must be equal')

        try:
            user = User.objects.get(email=email)
            if user.is_verified is False:
                raise serializers.ValidationError('User must be verified to change password.')
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError('User with email does not exist')
        return data


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email', None)
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)

        try:
            user = User.objects.get(email=email)
            is_password_correct = user.check_password(old_password)
            if not is_password_correct:
                raise serializers.ValidationError('Old password is wrong')
            if not user.is_verified:
                raise serializers.ValidationError('User is not verified')
            data['user'] = user
        except User.DoesNotExist as identifier:
            raise serializers.ValidationError('User with email does not exist')
        return data
        

