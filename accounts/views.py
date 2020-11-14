from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_q.tasks import async_task

from accounts.models import User
from accounts.serializers import UserSerializer, SignupSerializer, ActivateUserSerilaizer, FullUserSerializer, \
    ForgotPasswordSerializer, ChangePasswordSerializer, UpdatePasswordSerializer
from accounts.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from accounts import utils as u
from accounts import mails

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
    
    # @action(methods=['post'], detail=False, url_path='google', permission_classes=[AllowAny])
    # def google_signup(self, request):
    #     code = request.data.get('code')
    #     token_data = u.get_google_access_token(code)
    #     access_token = token_data.get('access_token')
    #     refresh_token = token_data.get('refresh_token')

    #     profile_data = u.get_google_profile(access_token)
    #     email = profile_data.get('email')
    #     google_id = profile_data.get('id')
    #     first_name = profile_data.get('given_name')
    #     last_name = profile_data.get('family_name')
    #     pic = profile_data.get('picture')
    #     link = profile_data.get('link')

    #     try:
    #         user = User.objects.get(email=email)
    #     except ObjectDoesNotExist:
    #         user = User.objects.create_user(email=email)
    #     contact = user.contact
    #     contact.first_name = first_name
    #     contact.last_name = last_name
    #     contact.save()

    #     avatar = u.get_image_from_url(pic)

    #     if avatar:
    #         contact.avatar.save(
    #             str(google_id) + '-avatar.jpg',
    #             avatar
    #         )

    #     try:
    #         contact_google = contact.social_profiles.get(
    #             user_id=google_id
    #         )
    #         contact_google.access_token = refresh_token
    #         contact_google.save()

    #     except ObjectDoesNotExist:
    #         ContactSocialProfile.objects.create(
    #             contact=contact,
    #             user_id=google_id,
    #             url=link,
    #             access_token=refresh_token,
    #             service=cc.GOOGLE
    #         )

    #     user.is_verified = True
    #     user.save()

    #     Token.objects.get_or_create(user=user)
    #     serializer = serializers.FullUserSerializer(user)

    #     return Response(
    #         {
    #             'results': serializer.data
    #         },
    #         status=status.HTTP_201_CREATED
    #     )
    
    @action(methods=['post'], detail=False, url_path='signup', permission_classes=[AllowAny])
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                user.verification_pin = u.get_verification_code()
                user.save()
                async_task(
                    'accounts.mails.send_formatted_email',
                    user=user)
                user_data = serializer.data
                user_data['verification_pin'] = user.verification_pin
            return Response(
                {
                    'results': user_data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': user_data.errors
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

    @action(methods=['post'], detail=False, url_path='update-password', permission_classes=[IsAuthenticated])
    def update_password(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            async_task('accounts.mails.send_update_password_email', user=user)
            serializer_data = FullUserSerializer(user)
            return Response(
                {
                    'results': serializer_data.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

    @action(methods=['post'], detail=False, url_path='verify-forgot-password', permission_classes=[AllowAny])
    def verify_forgot_password(self, request):
        serializer = ActivateUserSerilaizer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_verified = True
            user.save()
            serializer_data = FullUserSerializer(user)
            return Response(
                {
                    "results": serializer_data.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

    @action(methods=['post'], detail=False, url_path='verify-user', permission_classes=[AllowAny])
    def verify(self, request):
        serializer = ActivateUserSerilaizer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_verified = True
            user.save()
            token = Token.objects.get_or_create(user=user)
            async_task('accounts.mails.send_verification_email', user=user)
            serializer_data = FullUserSerializer(user)
            return Response(
                {
                    "results": serializer_data.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(methods=['post'], detail=False, url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user:
            if not user.is_verified:
                return Response(
                    {
                        'errors': 'This user is not verified'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FullUserSerializer(user)
            return Response(
                {
                    'results': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': 'User email or password is wrong'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    # def signup(self, request):
    #     serializer = RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         user_serializer = self.serializer_class(user)
    #         return Response(
    #             {
    #                 'results': user_serializer.data
    #             },
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         {
    #             'error': serializer.errors
    #         }
    #     )

    @action(methods=['post'], detail=False, url_path='forgot-password', permission_classes=[AllowAny])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.verification_pin = u.get_verification_code()
            user.save()
            async_task('accounts.mails.send_forgot_password_email', user=user)
            serialized_data = UserSerializer(user)
            return Response(
                {
                    'results': serialized_data.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def facebook_signup(self, request):
        pass


    @action(methods=['post'], detail=False, url_path='change-password', permission_classes=[AllowAny])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            token = Token.objects.get_or_create(user=user)
            async_task('accounts.mails.send_change_password_email', user=user)
            serializer_data = FullUserSerializer(user)
            return Response(
                {
                    'results': serializer_data.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

