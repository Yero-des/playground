from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan, Recommendation

# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loan)
admin.site.register(Recommendation)