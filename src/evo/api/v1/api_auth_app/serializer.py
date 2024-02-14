from rest_framework import serializers

class AuthorizationUserSerializer(serializers.Serializer): 
    username = serializers.CharField(label='Username')
    password = serializers.CharField(label='Password')

class ResetPasswordSerializer(serializers.Serializer): 
    email = serializers.EmailField(label='Email')