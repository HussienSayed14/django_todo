from django.urls import path
from . import views


urlpatterns = [
    path("tasks/", views.get_tasks, name="get_tasks"),
    path("tasks/create/",views.create_task , name="create_task"),
    path("tasks/register/",views.registet_user , name="register_user"),
    path("tasks/login/",views.login_user , name="login_user")

]