from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication_app.models import CustomUser

from constants import error_messages, status_response
from .serializer import AuthorizationUserSerializer, ResetPasswordSerializer
from .utils import reset_password_user, create_response

class AuthorizationUserAPI(APIView):
    def post(self, request):
        serializer = AuthorizationUserSerializer(data=request.data)
        if not serializer.is_valid():
            return create_response(status_response.ERROR, error_messages.ERROR_USER_NOT_FOUND)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if not (username and password): 
            return create_response(status_response.ERROR, error_messages.ERROR_USER_NOT_FOUND)

        user = authenticate(request=request, username=username, password=password)
        if user is None: 
            return create_response(status_response.ERROR, error_messages.ERROR_USER_NOT_FOUND)
        
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response(data={
            'status': status_response.SUCCESS, 
            'token': token.key,
            'created_at': token.created,
            'is_a_new_token': created
        })

class ResetPasswordUserAPI(APIView):
    def post(self, request): 
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return create_response(status_response.ERROR, error_messages.ERROR_USER_INVALID_EMAIL)

        email = serializer.validated_data['email']
        try: 
            user = CustomUser.objects.get(email=email)
            if not user.is_verified_email: 
                return create_response(status_response.ERROR, error_messages.ERROR_USER_NOT_VERIFIED_EMAIL)
            
            # send otp
            result = reset_password_user(user=user)
            
            return create_response(status_response.SUCCESS)
        except CustomUser.DoesNotExist:
            return create_response(status_response.ERROR, error_messages.ERROR_USER_NOT_FOUND_EMAIL)