from rest_framework import serializers
from todo_app.models import Task, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model, including additional fields."""

    class Meta:
        model = CustomUser
        fields = ["id", "username", "phone_number", "date_of_birth"]


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task model."""

    class Meta:
        model = Task
        fields = ["id", "title", "created_at", "due_date", "status"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """Handles input validation but NOT user creation."""
    
    password = serializers.CharField(write_only=True, min_length=6) # The write_only make the field accepted in POST but hidden in the Fetching

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "phone_number", "date_of_birth"]