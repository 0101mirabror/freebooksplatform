from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from . import models, forms
from django.views import View
from .utility import get_file_size
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Book
    
from django.http import HttpResponse, HttpResponseRedirect

class BookListView(ListView):
    model = models.Book
    template_name = "book_list.html"
    paginate_by = 4
    context_object_name = "books"

    def get_queryset(self):
        queryset = super().get_queryset()
        ordered_queryset = queryset.order_by('title')  # Replace 'title' with the desired field
        return ordered_queryset
    
    def get_context_data(self, **kwargs: Any):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['authors'] = models.Author.objects.all()
        context['genres'] = models.Author.objects.all()
        return context

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

class BookDetailView(DetailView):
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
        context['users'] = models.CustomUser.objects.all()
        print((self.request.user), '\n\n\n\n\n')
        context['current'] = models.CustomUser.objects.get(username=str(self.request.user))
        context['comments'] = models.Feedback.objects.filter(book=book)
        return context


class SaveCommentView(View):
    model = models.Feedback
    fields = ['user', 'book', 'email', 'rate', 'feedback']

    def post(self, request, *args, **kwargs):
        # Process the comment data here
        print(request.POST)
        user = request.user
        rate = request.POST.get('rate')
        book = request.POST.get('book')
        book1 = Book.objects.get(id=int(book))
        email = request.POST.get('email')
        comment = request.POST.get('feedback')
        feedback = models.Feedback(user=user, rate=int(rate), book=book1, email=email,   feedback=comment)
        feedback.save()
         
        
       
        # HttpResponseRedirect(reverse('your_url_name')) //alternatively
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Replace with your desired URL

    def get(self, request, *args, **kwargs):
        # Handle GET requests if needed
        # ...

        # Return an appropriate HttpResponse object
        return HttpResponse("This is a GET request")  # Replace with your desired response

def save_comment(request):
    print(request.method)
    form = forms.FeedbackForm(request.POST)

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
    model = Book
    # Replace with the fields you want to edit
    fields = ['title', 'duration', 'image', 'category', 'pdf', ]  
    # Replace with the name of your template
    template_name = 'edit_book.html'
    def get_success_url(self):
        return reverse_lazy('bookhiveapp:book_detail', kwargs={'pk': self.object.pk})

# view displays all genre's list
class GenresView(TemplateView):
    template_name = 'genres.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dic = {
            'badiiy': models.Book.objects.filter(category="RM").count(),
            'diniy':  models.Book.objects.filter(category="CM").count(),
            'maktab': models.Book.objects.filter(category="MD").count(),
            'bolalar':models.Book.objects.filter(category="SH").count(),      
            'biografiya': models.Book.objects.filter(category="BI").count(),
            'biznes':  models.Book.objects.filter(category="CR").count(),
            'technology': models.Book.objects.filter(category="TC").count(),
            'sanat':models.Book.objects.filter(category="AT").count(),      
            'sogliq': models.Book.objects.filter(category="HC").count(),
            'shahsiy':  models.Book.objects.filter(category="PG").count(),
            'ilmiy': models.Book.objects.filter(category="SR").count(),
            'siyosat':models.Book.objects.filter(category="ST").count(),      
        }
        context['quantity'] = dic
        return context
    
# view filters books by author and category  
def filter_books(request):
    title = request.GET.get('title')
    author = request.GET.get('author')
    genre = request.GET.get('category')
    views_count = request.GET.get('views_count')
    books = Book.objects.all()
    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__firstname__icontains=author)
    if genre:
        books = books.filter(category__icontains=genre)
    if views_count:
        books = books.filter(views_count=views_count)
    return render(request, 'filtered_books.html', {'books': books,})




