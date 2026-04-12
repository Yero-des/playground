from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class TestTemplateView(TemplateView, LoginRequiredMixin):
    template_name = 'tests/index.html'