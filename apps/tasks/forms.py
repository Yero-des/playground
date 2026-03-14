from django import forms
from .models import Task

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('content', 'completed')
        labels = {
            'content': 'Titulo de la tarea',
            'completed': 'Esta completado?'
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Titulo de tarea',
                'class': 'form-control'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    