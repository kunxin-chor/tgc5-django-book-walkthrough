from django.db import models
from books.models import Book
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    posted_when = models.DateTimeField(blank=False, auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " for book: " + self.book.title

