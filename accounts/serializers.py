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
