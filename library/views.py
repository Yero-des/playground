from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from library.models import Author, Book
from django.db.models import Count, Sum, Avg, Q
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    
    try:
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
        
        print(query_params)
        
        query_string = query_params.urlencode()
        
        return render(request, 'library/index.html', {
            'name': 'Yeromi Zavala Castillo',            
            'books': page_obj,
            'query': query,
            'query_string': query_string
        })
        
    except Exception as e:
        print(e)
        return HttpResponseNotFound("Pagina no encontrada")
