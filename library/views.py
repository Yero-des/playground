from django.http import HttpResponse
from django.shortcuts import render
from library.models import Author, Book

# Create your views here.
def index(request):
    
    books = Book.objects.all()
    
    return render(request, 'library/index.html', {
        'name': 'Yeromi Zavala Castillo',
        'books': books
    })