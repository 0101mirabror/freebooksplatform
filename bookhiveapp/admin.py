from django.contrib import admin
from .models import Book, Author, Feedback
from django.contrib.auth.admin import UserAdmin
from django import forms

class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = [
        "id",
        "title",
        "author"
        
    ]
    widgets = {
            'image': forms.TextInput(attrs={'required': False} ) }

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Feedback)