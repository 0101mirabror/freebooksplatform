from rest_framework import serializers
from .models import Book
from markdownx.fields import MarkdownxFormField


class BookModelSerializer(serializers.ModelSerializer):
    description = MarkdownxFormField
    class Meta:
        model = Book
        fields = '__all__'
 
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'firstname', 'lastname', 'image']
