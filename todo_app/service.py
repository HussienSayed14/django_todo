

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from todo_app.models import CustomUser, Task


class TaskService:

    @staticmethod
    def get_tasks():
        """ Fetch All Tasks"""
        
        return Task.objects.all()
    


    @staticmethod
    def create_task(user, validated_data):
        """Creates a new task and assigns it to the logged-in user."""
        return Task.objects.create(user=user, **validated_data)
    


    
class UserService:

    @staticmethod
    def get_tokens_for_user(user):
        """Generates JWT access & refresh tokens for an authenticated user."""
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


    @staticmethod
    def create_user(validated_data):
        """Creates a user with a hashed password."""
        user = CustomUser(
            username=validated_data["username"],
            phone_number=validated_data.get("phone_number", ""),
            date_of_birth=validated_data.get("date_of_birth", None),
        )
        user.set_password(validated_data["password"])  # Hash the password
        user.save()
        return user
    
    @staticmethod
    def login_user(username, password):
        """Authenticates user and returns JWT tokens & user data."""
        if not username or not password:
            return {}, False, "Username and password are required."

        user = authenticate(username=username, password=password)

        if user:
            tokens = UserService.get_tokens_for_user(user)
            return {"user": user, "tokens": tokens}, True, "Success"
        
        return {},False ,"Invalid credentials"
    
