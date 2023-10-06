from django.contrib import admin
from .models import Book, Author
from django.contrib.auth.admin import UserAdmin

class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = [
        "id",
        "title",
        "author"
        
    ]  

admin.site.register(Book, BookAdmin)
admin.site.register(Author)