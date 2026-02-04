from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="library"),
    path('detail/<str:book_id>', views.book_detail, name="book_detail"),
    path('recomendar/<int:book_id>', views.add_review, name="recommend_book")
]
