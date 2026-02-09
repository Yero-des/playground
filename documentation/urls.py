from django.urls import path
from . import views

urlpatterns = [
    path('test', views.TestView.as_view(), name='test'),
    path('list', views.TestListView.as_view(), name='list'),
    path('async', views.AsyncView.as_view(), name="async")
]
