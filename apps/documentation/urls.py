from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'documentation'

urlpatterns = [
    path('', TemplateView.as_view(template_name='documentation/index.html'), name="index"),
    path('list', views.TestListView.as_view(), name='list'),
    path('async', views.AsyncView.as_view(), name="async")
]
