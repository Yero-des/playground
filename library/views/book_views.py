from django.urls import reverse_lazy
from library.forms import BookForm
from library.models import Book
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import When, Case
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView

User = get_user_model()
    
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "library/book_list.html"
    context_object_name = "books"
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')

        query = self.request.GET.get('query_search')
        date_start = self.request.GET.get('start')
        date_end = self.request.GET.get('end')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query)
            )

        if date_start and date_end:
            queryset = queryset.filter(
                publication_date__range=[date_start, date_end]
            )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book_id_last_3 = self.request.session.get('last_3_viewed_books', [])
        
        last_3_viewed_books = Book.objects.filter(id__in=book_id_last_3).order_by(
            Case(*[When(id=pk, then=pos) for pos, pk in enumerate(book_id_last_3)])
        )     
        
        query_search = self.request.GET.get('query_search')
        query_params = self.request.GET.copy()
        
        if "page" in query_params:            
            query_params.pop('page')
        
        query_string = query_params.urlencode()
        
        context['name'] = "Yeromi Zavala Castillo"
        context['query_search'] = query_search
        context['query_string'] = query_string
        context['last_3_viewed_books'] = last_3_viewed_books

        return context
    

class BookDetailView(
    LoginRequiredMixin, 
    PermissionRequiredMixin,
    DetailView
):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"
    permission_required = "library.view_book"
    # slug_field = "slug"
    # slug_url_kwarg = "slug"
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perm('library.view_book'):
            response = super().get(request, *args, **kwargs)
            last_3_books = request.session.get('last_3_viewed_books', [])

            if len(last_3_books) < 3 and self.object.id not in last_3_books:
                last_3_books.insert(0, self.object.id)
            elif len(last_3_books) == 3 and self.object.id not in last_3_books:
                last_3_books.pop()
                last_3_books.insert(0, self.object.id)
            elif len(last_3_books) == 3 and self.object.id in last_3_books:
                last_3_books.remove(self.object.id)
                last_3_books.insert(0, self.object.id)
            
            request.session['last_3_viewed_books'] = last_3_books
            return response
        else:
            return HttpResponseForbidden("Contenido no disponible")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.reviews.order_by('-created_at')
        paginator = Paginator(reviews, 5)
        page_number = self.request.GET.get('page_review')
        page_review_obj = paginator.get_page(page_number)
        
        query_params = self.request.GET.copy()
        if "page_review" in query_params:
            query_params.pop('page_review')
        
        query_string = query_params.urlencode() 
        
        context["reviews"] = page_review_obj
        context["query_string"] = query_string
               
        return context


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/add_book.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Se ha agregado el nuevo libro")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al guardar el libro revisa los campos", "danger")
        return super().form_invalid(form)    
    
    
    def get_success_url(self):
        return reverse_lazy('book_list')
    
    
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/add_book.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(author__name=self.request.user.username)
    
    def form_valid(self, form):
        messages.success(self.request, "Se ha actualizado correctamente el libro correctamente", "warning")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar el libro revisa los campos", "danger")
        return super().form_invalid(form)    
    
    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={
            'pk': self.object.id
        })
     