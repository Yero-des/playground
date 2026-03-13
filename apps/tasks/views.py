from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import TaskForm

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'
    success_url = reverse_lazy('tasks:list_tasks')
    
    def form_valid(self, form):
        messages.success(self.request, "Tarea agregada correctamente.")
        return super().form_valid(form)
    

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:list_tasks')
    context_object_name = 'task'
    
    def form_valid(self, form):
        title = self.object.title
        messages.info(self.request, f'Se ha borrado la tarea "{title}".')
        return super().form_valid(form)
    