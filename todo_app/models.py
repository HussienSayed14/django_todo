from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings



# Create your models here.

class CustomUser(AbstractUser):
    """Extends Django's default user model with custom fields."""
    
    phone_number = models.CharField(max_length=15, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)

    """ Multi Column index
    class Meta:
        indexes = [
            models.Index(fields=["phone_number", "date_of_birth"]),  
        ]
    
    """

    def __str__(self):
        return self.username
    



class Task(models.Model):
    """Represents a task with a title, description, and status."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="tasks")
    

    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, db_index=True)

    
    def __str__(self):
        return f"{self.title}"

