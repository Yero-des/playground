import asyncio
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from library.models import Book
from django.http import HttpResponse
from django.views import View

# Create your views here.
class TestView(TemplateView):
    template_name = "documentation/test.html"
    
class TestListView(ListView):
    model = Book
    template_name = "documentation/book_list.html"
    context_object_name = "books"
    paginate_by = 5
    
class AsyncView(View):
    async def get(self, request, *args, **kwargs):
        # Perform io-blocking view logic using await, sleep for example.
        await asyncio.sleep(1)
        return HttpResponse("Hello async world!")