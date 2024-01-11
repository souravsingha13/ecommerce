from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, PasswordChangeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_mail_to_client
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationView(APIView):
    def post(self,request):
        serializers = RegistrationSerializer(data=request.data)
        print(serializers)
        if serializers.is_valid():
            send_mail_to_client(request.user)
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
            auth_data = get_tokens_for_user(request.user)
            return Response({"message":"Successfully logged in",**auth_data},status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    def post(self,request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    def post(self,request):
        print(request.user)
        serializer = PasswordChangeSerializer(context = {'request':request}, data = request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print("after called is valid")
        print(serializer.is_valid(raise_exception=True))
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"message" : "Successfully change password"},status=status.HTTP_204_NO_CONTENT)
