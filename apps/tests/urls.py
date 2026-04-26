from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "tests"

urlpatterns = [
    path('', views.TestTemplateView.as_view(), name="index"),
    path('video/list/', views.VideoListview.as_view(), name="videos")
]
