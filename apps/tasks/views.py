import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, DeleteView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import TaskForm

# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)    
    
 
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'
    success_url = reverse_lazy('tasks:list_tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Tarea agregada correctamente.")
        return super().form_valid(form)
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:list_tasks')
    context_object_name = 'task'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def form_valid(self, form):
        content = self.object.content
        messages.info(self.request, f'Se ha borrado la tarea "{content}".')
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'
    success_url = reverse_lazy('tasks:list_tasks')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_updated': True
        })
        return context
    
    def form_valid(self, form):
        messages.warning(self.request, f'La tarea "{self.object.content}" se actualizo correctamente.')
        return super().form_valid(form)
    

class MarkTaskView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            task_id = data.get('taskId', '')
            completed = str(data.get('completed', ''))
            
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task.completed = (completed == "True")
            task.save()
            
            if task.user != request.user:
                return JsonResponse({'status': 'forbidden'}, status=403)
                
            return JsonResponse({
                'status': 'ok',
                'object_id': task_id,
                'completed': (completed == "True")
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'messages': str(e),
            }, status=400)