from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import Book, Author
from .forms import BookForm, AuthorForm


# Create your views here.
def index(request):
    books = Book.objects.all()
    return render(request, 'books/index.template.html', {
        'all_books': books
    })


def create_book(request):
    # detect whether the user is viewing the form or submitting the form
    if request.method == 'POST':
        # if the method is POST, then the user has submitted the form

        # extract the submitted data from POST and populate the form
        form = BookForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            # if valid, save the data in the form
            form.save()

            # redirect back to the URL for the index view function
            return redirect(reverse(index))
        else:
            return render(request, 'books/create.template.html', {
                'form': form
            })
    else:
        # not POST, s must be GET, so we will just display the form
        create_form = BookForm()
        return render(request, 'books/create.template.html', {
            'form': create_form
        })


def view_authors(request):
    authors = Author.objects.all()
    return render(request, 'books/authors.template.html', {
        'authors': authors
    })


def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(view_authors))
        else:
            return render(request, 'books/create_author.template.html', {
                'form': form
            })
    else:
        # let the user view the form
        create_author_form = AuthorForm()
        return render(request, 'books/create_author.template.html', {
            'form': create_author_form
        })

