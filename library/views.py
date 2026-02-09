import time
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
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
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import When, Case

User = get_user_model()

class HelloTemplateView(TemplateView):
    template_name = 'library/hello.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["greeting"] = "hello world".capitalize()
        context["language"] = "ingles"
        context["lorem"] = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Sed obcaecati repellat voluptas error excepturi. Recusandae necessitatibus molestias autem sit? Cumque nostrum magnam necessitatibus nemo fugiat dolorum pariatur nam quae doloremque!"
        return context

class HelloView(View):
    def get(self, request):
        name = request.GET.get('name')
        return HttpResponse(f"Hola mundo desde CBV and my name is {name}")
 
    
class WelcomeView(TemplateView):
    template_name = 'library/welcome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_books"] = Book.objects.count()
        context["name"] = self.request.GET.get('name')
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
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        request.session['last_viewed_book'] = self.object.id
        return response

    
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "library/add_review.html"

    def form_valid(self, form):
        book_id = self.kwargs.get('pk')
        book = Book.objects.get(pk=book_id)
        form.instance.book = book
        form.instance.user_id = self.request.user.id
        
        would_recommend = form.cleaned_data.get('would_recommend')
        if would_recommend:
            messages.success(self.request, "Gracias por la reseña y recomendacion de nuestros libros 🤗")
        else:                                    
            messages.success(self.request, "Gracias por la reseña")
        
        return super().form_valid(form)  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('pk')
        book = Book.objects.get(pk=book_id)
        context["book"] = book
        return context         
    
    def get_success_url(self):
        return reverse_lazy("detail", kwargs={
            "book_id": self.kwargs.get("pk")
        })
    

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "library/add_review.html"
    
    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)

    def form_valid(self, form):
        would_recommend = form.cleaned_data.get('would_recommend')
        if would_recommend:
            messages.success(self.request, "Se actualizo su reseña gracias por la recomendación 🤗", "warning")
        else:                                    
            messages.success(self.request, "Se actualizo la reseña", "warning")
        
        return super().form_valid(form)  
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al guardar los cambios")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = Review.objects.get(pk=self.kwargs.get('pk'))
        context["book"] = review.book
        return context         
    
    def get_success_url(self):
        review = Review.objects.get(pk=self.kwargs.get("pk"))
        return reverse_lazy("detail", kwargs={
            "book_id": review.book.id
        })
     
  
class ReviewDeleteview(DeleteView):
    model = Review
    template_name = "library/review_confirm_delete.html"
    context_object_name = "review"
    
    def form_valid(self, form):
        messages.success(self.request, "Tu reseña fue eliminada", "danger")
        return super().form_valid(form)
    
    
    def get_success_url(self):
        review = Review.objects.get(pk=self.kwargs.get('pk'))
        return reverse_lazy("detail", kwargs={
            "book_id": review.book.id
        })
  
    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)
 
 
def home(request):
    print(request.user)
    return HttpResponse("Hola")


def index(request):
    
    books = Book.objects.all().order_by('-publication_date')
    query = request.GET.get('query_search')
    date_start = request.GET.get('start')
    date_end = request.GET.get('end')
    book_id_last_3 = request.session.get('last_3_viewed_books', [])
    
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
    
    print(book_id_last_3)
    last_3_viewed_books = Book.objects.filter(id__in=book_id_last_3).order_by(
        Case(*[When(id=pk, then=pos) for pos, pk in enumerate(book_id_last_3)])
        )        
            
    return render(request, 'library/index.html', {
        'name': 'Yeromi Zavala Castillo',            
        'books': page_obj,
        'query': query,
        'query_string': query_string,
        'last_3_viewed_books': last_3_viewed_books
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
    
    last_3_books = request.session.get('last_3_viewed_books', [])

    if len(last_3_books) < 3 and book.id not in last_3_books:
        last_3_books.insert(0, book.id)
    elif len(last_3_books) == 3 and book.id not in last_3_books:
        last_3_books.pop()
        last_3_books.insert(0, book.id)
    elif len(last_3_books) == 3 and book.id in last_3_books:
        last_3_books.remove(book.id)
        last_3_books.insert(0, book.id)
    
    request.session['last_3_viewed_books'] = last_3_books
    
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
            return redirect('detail', book_id=book.id)
        else:
            messages.error(request, "Corrige los errores del formulario",  "danger")
            
    return render(request, 'library/add_review.html', {
        "form": form,
        "book": book
    })
    

def time_test(request):
    time.sleep(2)
    return HttpResponse("Esta vista tardo 2 segundos")

class CounterTemplateView(TemplateView):
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