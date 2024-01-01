from django.shortcuts import render
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
        
