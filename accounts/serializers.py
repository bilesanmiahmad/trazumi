from rest_framework import serializers
from .models import User, Profile


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


class FullUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'verification_pin', 'auth_token']


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
        elif password is not confirm_password:
            raise serializers.ValidationError('Passwords must be equal')

        try:
            user = User.objects.get(email=email)
            if user.is_verified is False:
                raise serializers.ValidationError('User must be verified to change password.')
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError('User with email does not exist')
        return data