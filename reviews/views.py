from django.shortcuts import render, redirect, reverse
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def index(request):
    # return HttpResponse("Welcome to reviews")
    return render(request, 'reviews/index.template.html')


@login_required
def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user
            review.save()
            return redirect(reverse(index))
        else:
            return render(request, 'reviews/create.template.html', {
                'form': form
            })
    else:
        form = ReviewForm()
        return render(request, 'reviews/create.template.html', {
            'form': form
        })
