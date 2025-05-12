from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import (
    SystemProfile, SystemAccount
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # Create wallet automatically
        SystemAccount.objects.create(user=user)
        return user


class SystemProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class SystemAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAccount
        fields = ['id', 'balance', 'created_at', 'updated_at']
        read_only_fields = ['balance', 'created_at', 'updated_at']
