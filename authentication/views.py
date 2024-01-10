from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, PasswordChangeSerializer

class RegistrationView(APIView):
    def post(self,request):
        serializers = RegistrationSerializer(data=request.data)
        print(serializers)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request, format = None):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email = email,password = password)
        if user is not None:
            print(user)
            login(request, user)
            return Response("Successfully logged in", status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    def post(self,request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    def post(self,request):
        serializer = PasswordChangeSerializer(context = {'request':request}, data = request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
