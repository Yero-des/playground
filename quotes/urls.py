from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:number1>/<int:number2>', views.sum_of_two_numbers, name="sum-of-two-numbers"),
    path('<int:day>', views.days_week_with_number),
    path('<str:day>', views.days_week, name="day-quote"),
]
