from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from accounts.models import CustomUser
CHOOSE_CATEGORY = (
    ('RM', 'BADIIY'),
    ('CM', 'DINIY'),
    ('MD', 'MAKTAB DARSLIKLARI'),
    ('SH', 'BOLALAR')
)
class Author(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    life = models.TextField()
    image = models.ImageField(upload_to='author_images', default="author_images/images.png", null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    books_number = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.firstname)
        super(Author, self).save(*args, **kwargs)


    def __str__(self):
        return self.firstname

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.IntegerField()
    image = models.ImageField(upload_to='media/books', null=True, blank=True, default="media/books/bookwithoutcover.jpg")
    category = models.CharField(choices=CHOOSE_CATEGORY, max_length=4)
    pdf = models.FileField(upload_to="pdf_books")
    views_count = models.IntegerField(null=True, blank=True, default=0)
    
    def __str__(self):
        return self.title
    
class UserData(models.Model):
    user = models.TextField(default=None)
    
    def __str__(self):
        return self.user
    
class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    email = models.EmailField()
    feedback = models.TextField()
    
    def __str__(self):
        return self.user
    