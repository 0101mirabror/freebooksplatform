from django.urls import path, include
from . import views
from django.conf.urls import handler404

handler404 = 'bookhiveapp.views.custom_404'
app_name="bookhiveapp"
urlpatterns = [
    path('', views.BookListView.as_view() ,name="books_list"),
    path('authors/', views.AuthorListView.as_view() ,name="authors_list"),
    path('book/<int:pk>',  views.BookDetailView.as_view() ,name="book_detail"),
    path('author/<slug:slug>',  views.AuthorDetailView.as_view() ,name="author_detail"),
    path('category/<str:category>',  views.BookCategory.as_view() ,name="book_category"),
    path('search/book/',  views.BookSearchView.as_view() ,name="book_search"),
    path('addbook/',  views.AddBookView.as_view() ,name="add_book"),
    path('savebook/',  views.book_post ,name="save_book"),
    path('savecomment/',  views.SaveCommentView.as_view() ,name="save_comment"),
    path('book/product/<int:pk>/payment',  views.book_payment ,name="payment"),
    path('book/<int:pk>/edit/', views.BookModelUpdateView.as_view(), name='book_edit'),
    path('genres/', views.GenresView.as_view(), name='books_genres'),
    path('filter/', views.filter_books, name='filter_books'),
    path('pdfviewer/', views.show_pdf, name='pdf_viewer'),
   
    
]