from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Task
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    

class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/add_task.html'
    fields = ('title', 'completed')
    
    def form_valid(self, form):
        messages.success(self.request, "Tarea agregada correctamnte.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tasks:list_tasks')
    