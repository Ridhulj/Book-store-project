from django import forms
from .models import Book,Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets={
            'title':forms.TimeInput(attrs={'class':'form-control','placeholder':'Enter the book name'}),
            'author': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select the author name'}),
            'price': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Enter the book price'}),
        }