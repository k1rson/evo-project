from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication_app.models import CustomUser

from constants import error_messages
from .serializer import AuthorizationUserSerializer, ResetPasswordSerializer
from .utils import reset_password_user

class AuthorizationUserAPI(APIView):
    def post(self, request):
        serializer = AuthorizationUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'success': False,
                'err_msg': error_messages.ERROR_AUTH_APP_INCORRECT_DATA
            }, status=status.HTTP_200_OK)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        if not (username and password): 
            return Response(data={
                'success': False, 
                'err_msg': error_messages.ERROR_AUTH_APP_INCORRECT_DATA
            }, status=status.HTTP_200_OK)

        user = authenticate(request=request, username=username, password=password)
        if user is None: 
            return Response(data={
                'success': False,
                'err_msg': error_messages.ERROR_AUTH_APP_USER_NOT_FOUND_OR_DEACTIVATE
            }, status=status.HTTP_200_OK)
        
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response(data={
            'success': True, 
            'token': token.key,
            'created_at': token.created,
            'is_a_new_token': created
        })

class ResetPasswordUserAPI(APIView):
    def post(self, request): 
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'success': False, 
                'err_msg': error_messages.ERROR_AUTH_APP_INVALID_EMAIL
            })

        email = serializer.validated_data.get('email')
        try: 
            user = CustomUser.objects.get(email=email)
            if not user.is_verified_email: 
                return Response(data={
                    'success': False, 
                    'err_msg': error_messages.ERROR_AUTH_APP_NOT_VERIFIED_EMAIL
                })
            
            # send otp
            result = reset_password_user(user=user)
            ...
            
        except CustomUser.DoesNotExist:
            return Response(data={
                'success': False, 
                'err_msg': error_messages.ERROR_AUTH_APP_USER_WITH_CURRENT_EMAIL_NOT_FOUND
            })