from django.urls import reverse_lazy
from ..forms import ReviewForm
from library.models import Author, Book, Review
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

class ReviewCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "library/add_review.html"
    permission_required = "library.add_review"

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
        return reverse_lazy("book_detail", kwargs={
            "pk": self.kwargs.get("pk")
        })
    

class ReviewUpdateView(LoginRequiredMixin, UpdateView):    
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
        return reverse_lazy("book_detail", kwargs={
            "pk": review.book.id
        })
     
  
class ReviewDeleteview(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_review"
    model = Review
    template_name = "library/review_confirm_delete.html"
    context_object_name = "review"
    
    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)
    
    def get_success_url(self):
        review = Review.objects.get(pk=self.kwargs.get('pk'))
        return reverse_lazy("book_detail", kwargs={
            "pk": review.book.id
        })
        
    def form_valid(self, form):
        messages.success(self.request, "Tu reseña fue eliminada", "danger")
        return super().form_valid(form)
    
    
  
