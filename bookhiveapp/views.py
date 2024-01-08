from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from. import models
 

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
    
    # def get(self, request, pk, *args, **kwargs):
    #     def get_ip(request):
    #         adress = request.META.get('HTTP_X_FORWARDED_FOR')
    #         # print(request.META)
    #         if adress:
    #             ip = adress.split(',')[-1].strip()
    #             print(adress.split(',')[-1].strip(), '\n\n\n')
    #         else:
    #             ip = request.META.get('REMOTE_ADDR')
    #         return ip
    #     ip = get_ip(request)
    #     u = models.UserData(user=ip)
    #     print("ip address:", ip)
    #     result = models.UserData.objects.filter(Q(user__icontains=ip))
    #     if len(result) == 1:
    #         print("user exists")
    #     elif len(result) > 1:
    #         print('user exists')        
    #     else:
    #         u.save()
    #         print('user is unique')
    #     count = models.UserData.objects.all().count()
    #     print("total users count is ", count)
    #     return render(request, 'book_detail.html', {'count': count})

class AuthorListView(ListView):
    model = models.Author
    template_name = "author_list.html"

    # def get_context_data(self,request, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     author_instance = models.Author.objects.get(pk=)
    #     books = models.Book.objects.filter
    #     context[''] = 1
    #     return context

    # def get(self, request, *args, **kwargs):
    #     author = models.Author.objects.get()
 
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
        print(author,"\n\n\n\n\n\n\n\n", request.POST, writer)
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

    # def get_context_data(self, **kwargs):
    #     context = super(BookCategory, self).get_context_data(**kwargs)
    #     context['book_category'] = self.category
    #     return context

def book_payment(request, pk):
    context = {

    }
    return render(request, "payment.html", context)

# developmentda DEBUG=FALSE holatida ishlatish mumkin
def custom_404(request, exception):
    return render(request, "404.html", status=404)

<<<<<<< HEAD
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Book


# class based view for django edit -update model
class BookModelUpdateView(UpdateView):
    model = Book
    # fields = '__all__' # Replace with the fields you want to edit
    # exclude = ['owner', 'views_count']
    fields = ['title', 'duration', 'image', 'category', 'pdf', ]  # Replace with the fields you want to edit
    template_name = 'edit_book.html'  # Replace with the name of your template
    # success_url = reverse_lazy('books_list')  # Replace with the URL name of your success URL
    def get_success_url(self):
        return reverse_lazy('paginationapp:book_detail', kwargs={'pk': self.object.pk})
 

 
 


from django.views.generic import TemplateView

class GenresView(TemplateView):
    template_name = 'genres.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dic = {
            'badiiy': Book.objects.filter(category="RM").count(),
            'diniy': Book.objects.filter(category="CM").count(),
            'maktab': Book.objects.filter(category="MD").count(),
            'bolalar': Book.objects.filter(category="SH").count(),      
        }
        context['quantity'] = dic
        return context
=======
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
>>>>>>> version9




