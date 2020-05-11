from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    ISBN = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=False)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title + " (" + self.ISBN + ")"


class Author(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    dob = models.DateField(blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class Genre(models.Model):
    title = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.title