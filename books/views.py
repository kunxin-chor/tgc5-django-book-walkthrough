from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    # return HttpResponse("Hello")
    return render(request, 'books/index.template.html')