from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.WelcomeView.as_view(), name="welcome"),
    path('books/list', views.BookListView.as_view(), name="book_list"),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name="book_detail"),
    path('books/<int:pk>/review', views.ReviewCreateView.as_view(), name="add_review"),
    path('review/<int:pk>/edit', views.ReviewUpdateView.as_view(), name="edit_review"),
    path('review/<int:pk>/delete', views.ReviewDeleteview.as_view(), name="delete_review"),
    path('hello', views.HelloTemplateView.as_view(), name="hello"),
    path('recomendar/<int:book_id>', views.add_review, name="recommend_book"),
    path('time-test', views.time_test),
    path('counter', views.CounterTemplateView.as_view())
]
