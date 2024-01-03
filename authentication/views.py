from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer

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
        
