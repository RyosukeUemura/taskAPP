from django.urls import path

from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("task/<int:task_id>/complete/", views.complete_task, name="complete_task"),
]
