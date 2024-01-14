from rest_framework import serializers
from .models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        } 
    def save(self):
        user = User(email=self.validated_data['email'])
        print(user)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        print(user.email)
        return user

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    new_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    def validate_current_password(self, value):
        print("validate_current_password")
        print(self.context['request'].user)
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style = {'input_type' : 'password'}, write_only = True)
    password2 = serializers.CharField(max_length = 255, style = {'input_type' : 'password'}, write_only = True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match")

        return attrs