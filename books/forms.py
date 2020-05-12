from django import forms
from .models import Book, Author, Genre


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'ISBN', 'desc', 'genre', 'authors', 'owner', 'tags', 'cost')


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'dob', 'created_by')


class SearchBookForm(forms.Form):
    title = forms.CharField(required=False)
    genre = forms.ModelChoiceField(Genre.objects.all(), required=False)
    author = forms.CharField(required=False)
