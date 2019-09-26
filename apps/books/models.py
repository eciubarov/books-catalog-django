from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from config.storage import PublicMediaStorage
from sorl.thumbnail import get_thumbnail


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Category(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Cover(models.Model):
    file = models.ImageField(storage=PublicMediaStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def thumbnail(self):
        return get_thumbnail(self.file, '300x500', crop='center', quality=99).url


class Book(models.Model):
    cover = models.ForeignKey(Cover, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)

    def link(self):
        return reverse('books:item', args=[self.id])


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)


class ReadBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_date = models.DateField(auto_now_add=True)