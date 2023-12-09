"""DJANGO REST FRAMEWORK"""

from rest_framework import viewsets
from rest_framework import generics
 
from .serializers import BookModelSerializer, UserSerializer
from .models import Book
from accounts.models import CustomUser
 
# viewsets
class BookModelViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# apiviews
class BookModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer