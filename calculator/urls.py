from django.urls import path
from . import views

urlpatterns = [
    path('<str:symbol>/<int:num1>/<int:num2>', views.calculator, name='calculator')
]
