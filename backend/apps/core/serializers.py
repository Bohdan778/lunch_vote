from rest_framework import serializers
from .models import Restaurant, Menu, Employee, Vote
from django.contrib.auth import get_user_model

User = get_user_model()

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'created_at']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'items', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class EmployeeCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    legacy_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'legacy_token']

    def create(self, validated_data):
        password = validated_data.pop('password')
        token = None
        user = User(**validated_data)
        user.set_password(password)
        # генеруємо legacy token
        user.legacy_token = validated_data.get('legacy_token') or __import__('secrets').token_hex(32)
        user.save()
        return user

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'employee', 'menu', 'created_at']
        read_only_fields = ['created_at']
