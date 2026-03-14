from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name="list_tasks"),
    path('create/', views.TaskCreateView.as_view(), name="add_task"),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name="delete_task"),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name="update_task"),
    path('mark_task/', views.MarkTaskView.as_view(), name="mark_task")
]
