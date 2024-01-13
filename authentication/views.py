from django.contrib.auth import authenticate, login, logout
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, PasswordChangeSerializer
from .models import User
from django.conf import settings
import jwt
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect
from .utils import get_tokens_for_user, link_generator, send_email_to_client, password_reset_token_generator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator




class RegistrationView(APIView):
    def post(self,request):
        serializers = RegistrationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            user_data = serializers.data
            user = User.objects.get(email = user_data['email'])
            absurl = link_generator(request, user)
            send_email_to_client(user, absurl)
            return Response({"message":f"Go to this emali {serializers.data} to verify"}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id = payload["user_id"])
            if not user.is_active:
                user.is_active = True
                user.save()
            return redirect("http://localhost:8000/user/login")
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        

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
        serializer = PasswordChangeSerializer(context = {'request':request}, data = request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"message" : "Successfully change password"},status=status.HTTP_204_NO_CONTENT)
    
class PasswordResetView(APIView):
    def post(self, request):
        user_email = request.data.get('email')
        user = User.objects.filter(email = user_email)
        if user.exists():
            user = User.objects.get(email = user_email)
            absurl = password_reset_token_generator(self,request, user)
            send_email_to_client(user,absurl)
        return Response({"success": "We have sent you a link to reset your password"}, status=status.HTTP_200_OK)


class PasswordTokenCheckView(APIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)
            if PasswordResetTokenGenerator().check_token(user,token): 
                print("jsf") 
        except DjangoUnicodeDecodeError as identifier:
            return Response({"message":"this is from PasswordTokenCheckView"})