from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name="list_tasks"),
    path('create/', views.TaskCreateView.as_view(), name="add_task"),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name="delete_task"),
]
