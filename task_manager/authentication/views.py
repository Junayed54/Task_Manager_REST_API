from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, update_session_auth_hash
from rest_framework import generics,status
from rest_framework.authtoken.models import Token
from . import serializers
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


class Sign_up_api(generics.GenericAPIView):
    serializer_class=serializers.UserCreationSerializer


    def post(self,request):
        data=request.data

        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SigninAPIView(APIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        return Response(data={'detail': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class SignoutAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(data={'detail': 'Successfully signed out'}, status=status.HTTP_200_OK)
    
    
    
class PasswordChangeAPIView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordChangeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return Response(data={'detail': 'Password successfully changed'}, status=status.HTTP_200_OK)

        return Response(data={'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.UserProfileUpdateSerializer # Create this serializer in your serializers.py file
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'Profile successfully updated'}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)