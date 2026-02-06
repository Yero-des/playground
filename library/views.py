from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from .forms import ReviewForm
from library.models import Author, Book, Review
from django.db.models import Count, Sum, Avg, Q
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.templatetags.static import static
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

User = get_user_model()

def hello(request):
    return HttpResponse("Hola mundo desde FBV")


class HelloView(View):
    def get(self, request):
        name = request.GET.get('name')
        return HttpResponse(f"Hola mundo desde CBV and my name is {name}")
    
class WelcomeView(TemplateView):
    template_name = 'library/welcome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_books"] = Book.objects.count()
        return context
    
  
class BookListView(ListView):
    model = Book
    template_name = "library/book_list.html"
    context_object_name = "books"
    paginate_by = 5
    

class BookDetailView(DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"
    # slug_field = "slug"
    # slug_url_kwarg = "slug"
    
    
def index(request):
    
    books = Book.objects.all().order_by('-publication_date')
    query = request.GET.get('query_search')
    date_start = request.GET.get('start')
    date_end = request.GET.get('end')
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query)
        )
        
    if date_start and date_end:
        books = books.filter(
            publication_date__range=[
                date_start, date_end
            ]
        )
        
    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop('page')
    
    query_string = query_params.urlencode()
    
    return render(request, 'library/index.html', {
        'name': 'Yeromi Zavala Castillo',            
        'books': page_obj,
        'query': query,
        'query_string': query_string
    })
        

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.order_by('-created_at')
    
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page_review')
    page_review_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if "page_review" in query_params:
        query_params.pop('page_review')
    
    query_string = query_params.urlencode()
    
    return render(request, 'library/detail.html', {
        'book': book,
        'reviews': page_review_obj,
        'query_string': query_string
    })
    
    
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False) # Parar el guardado automatico
            review.book = book
            review.user = request.user
            review.save()
            
            would_recommend = form.cleaned_data.get('would_recommend')
            if would_recommend:
                messages.success(request, "Gracias por la reseña y recomendacion de nuestros libros 🤗")
            else:                                    
                messages.success(request, "Gracias por la reseña")
            return redirect('book_detail', book_id=book.id)
        else:
            messages.error(request, "Corrige los errores del formulario",  "danger")
            
    return render(request, 'library/add_review.html', {
        "form": form,
        "book": book
    })