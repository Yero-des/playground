from django.contrib import admin
from .models import Task
from django.core.checks import register

# Register your models here.
@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ('content', 'completed', 'created_at')