from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from pages.choices import * 


from django.contrib.auth.models import User
from pages.models import Book
from pages.models import Listing
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class ListForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=100)
    isbn = forms.CharField(max_length=13)
    edition = forms.CharField(max_length=5) #length here assumes no more than 999th edition -- seems like a reasonable assumption
    pub_year = forms.CharField(max_length=5) 
    condition = forms.ChoiceField(choices=CONDITION)
    class Meta:
        model=Book
        fields=['title', 'author', 'isbn', 'edition', 'pub_year']
        

