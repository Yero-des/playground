from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.WelcomeView.as_view(), name="welcome"),
    path('books/list', views.BookListView.as_view(), name="book_list"),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('books/add', views.BookCreateView.as_view(), name='add_book'),
    path('books/<int:pk>/edit', views.BookUpdateView.as_view(), name="edit_book"),
    path('books/<int:pk>/review', views.ReviewCreateView.as_view(), name="add_review"),
    path('review/<int:pk>/edit', views.ReviewUpdateView.as_view(), name="edit_review"),
    path('review/<int:pk>/delete', views.ReviewDeleteview.as_view(), name="delete_review"),
    path('hello', views.HelloTemplateView.as_view(), name="hello"),
    path('time-test', views.time_test),
    path('counter', views.CounterTemplateView.as_view())
]