from django.http import HttpResponse
from library.models import Book
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import time

class HelloTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'library/hello.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["greeting"] = "hello world".capitalize()
        context["language"] = "ingles"
        context["lorem"] = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Sed obcaecati repellat voluptas error excepturi. Recusandae necessitatibus molestias autem sit? Cumque nostrum magnam necessitatibus nemo fugiat dolorum pariatur nam quae doloremque!"
        return context


class HelloView(LoginRequiredMixin, View):
    def get(self, request):
        name = request.GET.get('name')
        return HttpResponse(f"Hola mundo desde CBV and my name is {name}")
 
    
class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'library/welcome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_books"] = Book.objects.count()
        context["name"] = self.request.GET.get('name')
        return context
    
    
class CounterTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'library/counter.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visits = self.request.session.get('visits', 0)
        visits += 1
        
        self.request.session['visits'] = visits
        # self.request.session.set_expiry(15)
        # 300 -> 10 min, 0 -> Al cerrar el navegador, None -> Duracion por defecto
        
        context['visits'] = visits
        return context 
       
@login_required
def time_test(request):
    time.sleep(2)
    return HttpResponse("Esta vista tardo 2 segundos")