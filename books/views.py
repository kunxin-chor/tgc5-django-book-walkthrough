from django.shortcuts import render, HttpResponse
from .models import Book, Author

# Create your views here.
def index(request):
    books = Book.objects.all()
    return render(request, 'books/index.template.html', {
        'all_books': books
    })


def view_authors(request):
    authors = Author.objects.all();
    return render(request,'books/authors.template.html', {
        'authors': authors
    })
