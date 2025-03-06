from todo_app.serializers import CustomUserSerializer, RegisterUserSerializer, TaskSerializer
from todo_app.service import TaskService, UserService
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

###################################### Tasks ######################################################################

@swagger_auto_schema(
    method='get',
    operation_description="Get all tasks for authenticated user",
    responses={200: TaskSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    """Fetch all tasks."""
    user = request.user
    print(f"User Data : {user}")
    tasks = TaskService.get_tasks()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new task",
    request_body=TaskSerializer,
    responses={
        201: TaskSerializer,
        400: openapi.Response(description="Bad Request"),
        500: openapi.Response(description="Something Wrong happened please try again.")
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    """Create Task tasks."""
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = TaskService.create_task(request.user, serializer.validated_data)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Get a specific task by ID",
    manual_parameters=[
        openapi.Parameter(
            'task_id',
            openapi.IN_PATH,
            description="ID of the task to retrieve",
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={
        200: TaskSerializer,
        400: openapi.Response(description="Task not found")
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task_by_id(request, task_id):
    task = TaskService.get_task_by_id(task_id)
    if not task:
        return Response({"error": "Task not found"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

################################################### AUTH ######################################################################

@swagger_auto_schema(
    method='post',
    operation_description="Register a new user",
    request_body=RegisterUserSerializer,
    responses={
        201: openapi.Response(
            description="User created successfully",
            schema=RegisterUserSerializer()
        ),
        400: openapi.Response(description="Bad Request")
    }
)
@api_view(["POST"])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = UserService.create_user(serializer.validated_data)
        tokens = UserService.get_tokens_for_user(user)
        return Response({
            "user": serializer.data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_description="Login user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Login successful",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                    }),
                    'tokens': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'access': openapi.Schema(type=openapi.TYPE_STRING),
                            'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                }
            )
        ),
        400: openapi.Response(description="Bad Request")
    }
)
@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    result, flag, message = UserService.login_user(username, password)
    if not flag:
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
    user_data = CustomUserSerializer(result["user"]).data
    return Response({"user": user_data, "tokens": result["tokens"]}, status=status.HTTP_200_OK)