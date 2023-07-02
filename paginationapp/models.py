from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    duration = models.IntegerField()
    image = models.ImageField(upload_to='media/books')

    def __str__(self):
        return self.title