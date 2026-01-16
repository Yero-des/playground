from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan, Recommendation
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from datetime import datetime

# Register your models here.

User = get_user_model()

admin.site.site_header = "Administrador MiniLibrary"
admin.site.site_title = "Minilibrary panel"
admin.site.index_title = "Bienvenidos al panel de minilibrary"

@admin.action(description="Marcar préstamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=True, return_date=datetime.now())
    
@admin.action(description="Desmarcar préstamos como no devueltos")
def desmark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=False, return_date=None)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

class RecomendationInline(admin.TabularInline):
    model = Recommendation
    extra = 1

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
    
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ('username', 'email', 'date_joined', 'is_superuser')
    ordering = ['-date_joined']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)
    list_filter = ('birth_date',)
    ordering = ['-birth_date']
    date_hierarchy = 'birth_date'
    
@admin.register(Genre)    
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookDetailInline, ReviewInline, RecomendationInline, LoanInline]
    list_display = ('title', 'author', 'publication_date', 'pages')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genres', 'publication_date')
    ordering = ['-publication_date']
    date_hierarchy = 'publication_date'
    autocomplete_fields = ['author', 'genres']
    
    fieldsets = (
        ("Información general", {
            "fields": ('title', 'author', 'publication_date', 'genres'),
        }),
        ("Detalles", {
            "fields": ('isbn', 'pages'),
            "classes": ('collapse', )
        }),
    )
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_staff
    
    
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ('loan_date', )
    list_display = ('user', 'book', 'loan_date', 'is_returned', 'return_date')
    ordering = ['-loan_date']
    actions = [mark_as_returned, desmark_as_returned]
    raw_id_fields = ['user', 'book']
    
    fieldsets = (
        ("Conexiones", {
            "fields": ('user', 'book',)
        }),
        ("Detalles opcionales", {
            "fields": ('return_date', 'is_returned', 'loan_date',),
            "classes": ('collapse',)
        }),
    )
    
@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'note')
    search_fields = ('user__name', 'book__title')
    date_hierarchy = 'recommended_at'
    
    fieldsets = (
        ("Conexiones", {
            "fields": ('user', 'book',)
        }),
        ("Nota", {
            "fields": ('note',)
        }),
    )
    

# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
# admin.site.register(Loan, LoanAdmin)
# admin.site.register(Recommendation, RecommendationAdmin)
# admin.site.register(User, CustomUserAdmin)