from django.urls import path
from . import views
from django.conf.urls import handler404

handler404 = 'paginationapp.views.custom_404'
app_name="paginationapp"
urlpatterns = [
    path('books/', views.BookListView.as_view() ,name="books_list"),
    path('authors/', views.AuthorListView.as_view() ,name="authors_list"),
    path('book/<int:pk>',  views.BookDetailView.as_view() ,name="book_detail"),
    path('author/<slug:slug>',  views.AuthorDetailView.as_view() ,name="author_detail"),
    path('category/<str:category>',  views.BookCategory.as_view() ,name="book_category"),
    path('search/book/',  views.BookSearchView.as_view() ,name="book_search"),
    path('addbook/',  views.AddBookView.as_view() ,name="add_book"),
    path('savebook/',  views.book_post ,name="save_book"),
    path('book/product/<int:pk>/payment',  views.book_payment ,name="payment"),
]