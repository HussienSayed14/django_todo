from django.shortcuts import render
from todo_app.serializers import CustomUserSerializer, RegisterUserSerializer, TaskSerializer
from todo_app.service import TaskService, UserService
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
def get_tokens_for_user(user):
    """Generates JWT tokens for an authenticated user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tasks():
    """Fetch all tasks."""
    tasks = TaskService.get_tasks()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    """Create Task tasks."""
    serializer = TaskSerializer(data=request.data)
    task = TaskService.create_task(request.user, serializer.data)
    return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)




@api_view(["POST"])
def registet_user(request):
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        user = UserService.create_user(serializer.validated_data)
        tokens = get_tokens_for_user(user)
        return Response({
            "user": serializer.data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    result, flag, message = UserService.login_user(username, password) 


    if not flag:
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
    
    user_data = CustomUserSerializer(result["user"]).data
    return Response({"user": user_data, "tokens": result["tokens"]}, status=status.HTTP_200_OK)





   