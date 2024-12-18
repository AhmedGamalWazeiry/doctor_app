from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RegisterSerializer, AddUser
from rest_framework import generics
from .models import User
from django.contrib.auth.models import Permission
from rest_framework.views import APIView
from drf_yasg import openapi
from django.conf import settings
import json
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Create new organization
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(email=request.data['username']).exists():
            return Response({
                'username': 'username already exists'
            })
        user = serializer.save()

        user.save()
         # Authenticate and log in the user
        login(request, user)

        # Create an authentication token for the user
        token = AuthToken.objects.create(user=user)

        # Return the token in the same format as the LoginAPI
        return Response({
            'token': token[1]
        })



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Request Login
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)