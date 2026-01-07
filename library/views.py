from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from library.models import Author, Book
from django.db.models import Count, Sum, Avg
from django.db import transaction
from django.db import IntegrityError

# Create your views here.
def index(request):
    
    try:
        with transaction.atomic():
            authors = Author.objects.all().annotate(num_books=Count('books')).annotate(total_pages_books=Sum('books__pages'))
            num_libros = Book.objects.aggregate(num_libros=Count('id'))['num_libros']
            total_sum_pages_libros = Book.objects.aggregate(total_sum_pages_libros=Sum('pages'))['total_sum_pages_libros']
            avg_pages_libros = "{:.2f}".format(Book.objects.aggregate(avg_pages_libros=Avg('pages'))['avg_pages_libros'])
            # Book.objects.create(title="Nuevo Libro", author=Author.objects.get(id=1), publication_date="1994-04-06", pages=800, isbn="10293847")
    
        return render(request, 'library/index.html', {
            'name': 'Yeromi Zavala Castillo',
            'authors': authors,
            'num_libros': num_libros,
            'total_sum_pages_libros': total_sum_pages_libros,
            'avg_pages_libros': avg_pages_libros
        })
        
    except IntegrityError:        
        return HttpResponseBadRequest("Hubo un error inesperado")
    