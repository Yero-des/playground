from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan, Recommendation

# Register your models here.

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    
class LoanInline(admin.TabularInline):
    model = Loan
    extra = 1
    
class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = "Detalle del libro"
    

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookDetailInline, ReviewInline, LoanInline]
    list_display = ('title', 'author', 'publication_date', 'pages')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genres', 'publication_date')
    ordering = ['-publication_date']
    date_hierarchy = 'publication_date'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)
    list_filter = ('birth_date',)
    ordering = ['-birth_date']
    date_hierarchy = 'birth_date'

# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loan)
admin.site.register(Recommendation)