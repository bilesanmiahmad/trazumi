from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from accounts.models import User
from accounts.serializers import UserSerializer, RegistrationSerializer
from accounts.permissions import IsLoggedInUserOrAdmin, IsAdminUser

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @action(methods=['post'], detail=False, url_path='google', permission_classes=[AllowAny])
    def google_signup(self, request):
        code = request.data.get('code')
        token_data = u.get_google_access_token(code)
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')

        profile_data = u.get_google_profile(access_token)
        email = profile_data.get('email')
        google_id = profile_data.get('id')
        first_name = profile_data.get('given_name')
        last_name = profile_data.get('family_name')
        pic = profile_data.get('picture')
        link = profile_data.get('link')

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = User.objects.create_user(email=email)
        contact = user.contact
        contact.first_name = first_name
        contact.last_name = last_name
        contact.save()

        avatar = u.get_image_from_url(pic)

        if avatar:
            contact.avatar.save(
                str(google_id) + '-avatar.jpg',
                avatar
            )

        try:
            contact_google = contact.social_profiles.get(
                user_id=google_id
            )
            contact_google.access_token = refresh_token
            contact_google.save()

        except ObjectDoesNotExist:
            ContactSocialProfile.objects.create(
                contact=contact,
                user_id=google_id,
                url=link,
                access_token=refresh_token,
                service=cc.GOOGLE
            )

        user.is_verified = True
        user.save()

        Token.objects.get_or_create(user=user)
        serializer = serializers.FullUserSerializer(user)

        return Response(
            {
                'results': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def signup(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = self.serializer_class(user)
            return Response(
                {
                    'results': user_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'error': serializer.errors
            }
        )

    def facebook_signup(self, request):
        pass

    def verify(self, request):
        pass