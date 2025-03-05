


from todo_project.todo_app.models import CustomUser, Task


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
    
