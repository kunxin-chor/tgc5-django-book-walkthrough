from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from .models import Book, Author
from .forms import BookForm, AuthorForm, SearchBookForm
from reviews.forms import ReviewForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q

# Create your views here.
def index(request):
    books = Book.objects.all()
    search_form = SearchBookForm(request.GET)

    # always true
    queries = ~Q(pk__in=[])

    if request.GET:
        if 'title' in request.GET and request.GET['title']:
            queries = queries & Q(title__icontains=request.GET['title'])


        if 'author' in request.GET and request.GET['author']:
            queries = queries & (Q(authors__first_name__icontains=request.GET['author']) | Q(authors__last_name__icontains=request.GET['author']))


        if 'genre' in request.GET and request.GET['genre']:
            queries = queries & Q(genre__in=request.GET['genre'])

    books = books.filter(queries)

    print(books.query)
    return render(request, 'books/index.template.html', {
        'all_books': books,
        'search_form': search_form
    })


@login_required
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


def update_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect(reverse(index))
        else:
            return render(request, 'books/update_book.template.html', {
                'form': form
            })
    else:
        form = BookForm(instance=book)
        return render(request, 'books/update_book.template.html', {
            'form': form
        })


def update_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return(redirect(reverse(view_authors)))
    else:
        form = AuthorForm(instance=author)
    return render(request, 'books/update_author.template.html', {
        'form': form
    })


def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect(reverse(index))

    return render(request, 'books/delete_book.template.html', {
        'book': book
    })


def delete_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    if request.method == "POST":
        author.delete()
        return redirect(reverse(view_authors))

    return render(request, 'books/delete_author.template.html', {
        'author': author
    })


def view_book_details(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    review_form = ReviewForm()
    return render(request, 'books/details.template.html', {
        'book': book,
        'review_form': review_form
    })