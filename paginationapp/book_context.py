from . import models

def count_author_books(request):
    books = 1
    return {'context': request.GET}