from rest_framework import serializers
from .models import User


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
    print(current_password,new_password)
    
    def validate_current_password(self, value):
        print("validate_current_password")
        print(self.context['request'].user)
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value