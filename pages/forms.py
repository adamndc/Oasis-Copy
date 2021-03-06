from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from pages.choices import * 


from django.contrib.auth.models import User
from pages.models import Book
from pages.models import Listing
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ChoiceField, CharField, MultipleChoiceField


class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    FirstName = forms.CharField(label="First Name")
    LastName = forms.CharField(label="Last Name")
    phone = forms.IntegerField(label="Phone Number")
    class Meta:
        model=User
        fields=['username','FirstName','LastName','email','phone','password1','password2']

class ListForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=100)
    isbn = forms.CharField(max_length=13)
    confirm_isbn = forms.CharField(max_length=13)
    edition = forms.CharField(max_length=5) #length here assumes no more than 999th edition -- seems like a reasonable assumption
    pub_year = forms.CharField(max_length=5) 
    condition = forms.ChoiceField(choices=CONDITION)
    price = forms.DecimalField(max_digits=6, decimal_places=2)
    box = forms.ChoiceField(choices=BOOL, label="Is this a donation?")
    class Meta:
        model=Book
        fields=['title', 'author', 'isbn', 'edition', 'pub_year']

class FilterForm(Form):
    CONDITION_CHOICES = ((0, 'All'), ('1', 'New'), ('2', 'Like New'), ('3', 'Lightly Used'),
             ('4', 'Moderately Used'), ('5', 'Heavily Used'))
    condition_field = ChoiceField(choices=CONDITION_CHOICES, required=False)
    title_field = forms.ModelChoiceField(queryset = Listing.objects.all().values_list('book__title', flat=True), empty_label='All',initial=0, required=False)
    author_field = forms.ModelChoiceField(queryset = Listing.objects.all().values_list('book__author', flat=True), empty_label='All',initial=0, required=False)
    edition_field = forms.ModelChoiceField(queryset = Listing.objects.all().values_list('book__edition',flat=True).distinct(), empty_label='All',initial=0, required=False)
