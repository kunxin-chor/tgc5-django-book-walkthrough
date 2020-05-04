from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    ISBN = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=False)

    def __str__(self):
        return self.title + " (" + self.ISBN + ")"


class Author(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    dob = models.DateField(blank=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

