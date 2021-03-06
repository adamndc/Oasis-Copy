from django.db import models
import uuid # Required for unique listings
from django.forms import ModelForm
from django.urls import reverse
from pages.choices import *
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


User = settings.AUTH_USER_MODEL




# Create your models here.

#class User(models.Model):
 #   email = models.EmailField(max_length=200)
 #   def __str__(self):
 #       return self.name


class Listing(models.Model):
    #fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique id for this listing')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                        default = 1,
                        null = True,
                        on_delete = models.SET_NULL
                        )
    price= models.DecimalField(max_digits=10, decimal_places=2)
    hide_listing = models.BooleanField(default=False)
    times_reported = models.SmallIntegerField(default=0)
    report = models.ForeignKey('ReportListing',null = True, on_delete = models.SET_NULL)

    # not yet sure how users work - may want users not to be a model and instead use django default user handling
    # posted_by = models.ForeignKey('User', on_delete=models.SET_NULL,null=True)


    condition = models.CharField(
        max_length=1,
        choices=CONDITION,
        blank=True,
        default=1,
        help_text='Book condition',
    )
    # not yet sure yet how to handle images
    # image =

    class Meta:
        ordering = ['-date_added']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('listings-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.id} ({self.book.title})'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    #if we decide to have a model for author:
    #author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    edition = models.CharField(max_length=5) #length here assumes no more than 999th edition -- seems like a reasonable assumption
    pub_year = models.SmallIntegerField()

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


#message thread
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique id for this conversation')
    seller = models.ForeignKey(User,
                        related_name='seller',
                        default = 1,
                        null = True,
                        on_delete = models.SET_NULL
                        )
    buyer = models.ForeignKey(User,
                        related_name='buyer',
                        default = 2,
                        null = True,
                        on_delete = models.SET_NULL
            )
    report = models.ForeignKey('ReportListing',null = True, on_delete = models.SET_NULL)
    state = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default=0,
        help_text='Conversation status',
    )
    listing = models.ForeignKey(Listing, null = True, on_delete = models.SET_NULL)


class Message(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sentby = models.ForeignKey(User,
                        default = 1,
                        null = True,
                        on_delete = models.SET_NULL
                        )
    conversation = models.ForeignKey(Conversation, default = 1, null=True, on_delete = models.SET_NULL)
    class Meta:
        ordering = ['-timestamp']

class ReportListing(models.Model):
    sent_by = models.ForeignKey(User, default = 1,
                        null = True,
                        on_delete = models.SET_NULL)
    date_reported = models.DateTimeField(auto_now_add=True)

class NumSearch(models.Model):
    count = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    buyer_rating = models.IntegerField(
        choices = RATINGS,
        default = 5,
    )
    seller_rating = models.IntegerField(
        choices = RATINGS,
        default = 5,
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Photo(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True) 
    title = models.CharField(max_length=100)
    photo = models.FileField()
