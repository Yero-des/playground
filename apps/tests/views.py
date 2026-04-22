from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .models import Video

class TestTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'tests/index.html'
    
    
class VideoListview(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'tests/video_list.html'
    context_object_name = "videos"