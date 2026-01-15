from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from library.models import Author, Book
from django.db.models import Count, Sum, Avg
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    
    try:
        authors = Author.objects.all().annotate(num_books=Count('books')).annotate(total_pages_books=Sum('books__pages'))
        num_libros = Book.objects.aggregate(num_libros=Count('id'))['num_libros']
        total_sum_pages_libros = Book.objects.aggregate(total_sum_pages_libros=Sum('pages'))['total_sum_pages_libros'] or 0
        avg_pages = Book.objects.aggregate(avg_pages=Avg("pages"))["avg_pages"] or 0
        avg_pages_libros = f"{avg_pages:.2f}"

        return render(request, 'library/index.html', {
            'name': 'Yeromi Zavala Castillo',
            'authors': authors,
            'num_libros': num_libros,
            'total_sum_pages_libros': total_sum_pages_libros,
            'avg_pages_libros': avg_pages_libros
        })
        
    except Exception:
        return HttpResponseNotFound("Pagina no encontrada")
