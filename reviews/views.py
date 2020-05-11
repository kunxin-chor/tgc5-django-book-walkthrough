from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ReviewForm
from books.models import Book
from .models import Review
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def index(request):
    reviews = Review.objects.all()
    reviews = reviews.filter(owner=request.user)
    # return HttpResponse("Welcome to reviews")
    return render(request, 'reviews/index.template.html', {
        'reviews': reviews
    })


@login_required
def create_review(request, book_id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user
            review.book = get_object_or_404(Book, pk=book_id)
            review.save()
            return redirect(reverse(index))
        else:
            return render(request, 'reviews/create.template.html', {
                'form': form
            })
