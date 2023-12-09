from django.views.generic import TemplateView
from django.db import models
from django.db.models.query import QuerySet
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic.edit import FormMixin
from typing import Any, Dict
from. import models
from .import forms
from .utility import get_file_size 
import os 

class BookListView(ListView):
    model = models.Book
    template_name = "book_list.html"
    paginate_by = 4

class AuthorDetailView(DetailView):
    model = models.Author
    template_name = "author_detail.html"

    def get_object(self): 
        self.slug = self.kwargs['slug']
        self.author = self.model.objects.filter(slug=self.slug)[0]
        return self.author
    
    def get_context_data(self, **kwargs: Any):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['booklist'] = models.Book.objects.filter(author=self.author).order_by('title')
        return context

class BookDetailView(DetailView, FormMixin):
    model = models.Book
    template_name = "book_detail.html"

    def get_queryset(self): 
        self.pk = self.kwargs['pk']
        object = self.model.objects.filter(pk=self.pk)
        return object
        
    def get_object(self):
        object  = super(BookDetailView, self).get_object()
        object.views_count += 1
        object.save()
        return object
    
    # send each book size to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = models.Book.objects.get(id=self.object.id)
        context['book_size'] = get_file_size(book.pdf.size)
        return context

class AuthorListView(ListView):
    model = models.Author
    template_name = "author_list.html"

class BookSearchView(ListView):
    model = models.Book
    template_name = 'book_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = models.Book.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list
   
class AuthorSearchView(ListView):
    model = models.Author
    template_name = 'author_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        if query:
            object_list = models.Author.objects.filter(firstname__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list

class BookCategory(ListView):
    model = models.Book
    template_name = 'book_list.html'
    paginate_by = 4

    def get_queryset(self):
        self.category = self.kwargs['category']
        movies = models.Book.objects.filter(category=self.category)
        return movies
    
class AddBookView(TemplateView):
    model = models.Book
    template_name = "add_book_form.html"
 
    def get_context_data(self, **kwargs):
        context =  super(AddBookView, self).get_context_data(**kwargs)
        context['authors'] = models.Author.objects.all()
        return context
    
def book_post(request, *args, **kwargs):
    if request.method == 'POST':
        owner = request.user
        writer = request.POST.get('author')
        author = models.Author.objects.get(firstname=writer)
        title = request.POST.get('title')  
        duration = request.POST.get('duration')  
        image = request.FILES.get('image')
        pdf = request.FILES.get('pdf')
        book = models.Book(owner=owner, author=author, title=title, duration=duration, image=image, pdf=pdf )
        book.save()
        messages.success(request, 'Book is saved successfully!')
        return redirect('/')
    else:
        messages.success(request, 'Book is not saved  successfully!!!')
        return redirect('/addbook')

def book_payment(request, pk):
    context = {

    }
    return render(request, "payment.html", context)

# developmentda DEBUG=FALSE holatida ishlatish mumkin
def custom_404(request, exception):
    return render(request, "404.html", status=404)

# class based view for django edit -update model
class BookModelUpdateView(UpdateView):
    model = models.Book
    # exclude = ['owner', 'views_count']
    fields = ['title', 'duration', 'image', 'category', 'pdf', ]  # Replace with the fields you want to edit
    template_name = 'edit_book.html'  # Replace with the name of your template
    def get_success_url(self):
        return reverse_lazy('bookhiveapp:book_detail', kwargs={'pk': self.object.pk})
 
class GenresView(TemplateView):
    template_name = 'genres.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dic = {
            'badiiy': models.Book.objects.filter(category="RM").count(),
            'diniy':  models.Book.objects.filter(category="CM").count(),
            'maktab': models.Book.objects.filter(category="MD").count(),
            'bolalar':models.Book.objects.filter(category="SH").count(),      
        }
        context['quantity'] = dic
        return context




