from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ReviewForm, CommentForm
from books.models import Book
from .models import Review
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

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


def view_review_details(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comment_form = CommentForm()
    return render(request, 'reviews/details.template.html', {
        'review': review,
        'comment_form': comment_form
    })


def process_create_comment(request, review_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.review = get_object_or_404(Review, pk=review_id)
            comment.save()
            messages.success(request, "New comment successfully added")
            return redirect(reverse('view_review_details_route', kwargs={'review_id':review_id}))
        else:
            messages.error(request, "Unable to add new comment")
            return redirect(reverse('view_review_details_route', review_id=review_id))