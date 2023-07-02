from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from. import models
class BookListView(ListView):
    model = models.Book
    template_name = "book_list.html"
    paginate_by = 4
