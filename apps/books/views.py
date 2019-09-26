from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.books.models import ReadBook
from apps.books.serializers import *
from apps.books.permissions import *


class BookList(View):
    def get(self, request):
        books = Book.objects.all().order_by('-id')
        return render(request, 'pages/home.html', locals())


class MyBookList(LoginRequiredMixin, View):
    def get(self, request):
        books = Book.objects.filter(publisher=request.user).order_by('-id')

        read_books = Book.objects.filter(
            id__in=[rbook.book.id for rbook in ReadBook.objects.filter(user=request.user)]
        )
        return render(request, 'pages/my-books.html', locals())


class BookView(View):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise Http404
        return render(request, 'pages/book-view.html', locals())


class BookAdd(LoginRequiredMixin, View):
    def get(self, request):
        page_title = 'Add a new book to the catalog'
        is_edit = 0
        book_id = 0
        return render(request, 'pages/add-book.html', locals())


class BookEdit(LoginRequiredMixin, View):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            page_title = 'Edit book "{}"'.format(book.title)
            is_edit = 1
            book_id = book.id
            if book.publisher != request.user:
                raise Http404

            return render(request, 'pages/add-book.html', locals())
        except Book.DoesNotExist:
            raise Http404


class BookDelete(LoginRequiredMixin, View):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            if book.publisher == request.user:
                book.delete()
                return redirect(reverse('books:my'))
            else:
                raise Http404
        except Book.DoesNotExist:
            raise Http404


class ReadBookView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            ReadBook.objects.create(book=book, user=request.user)
            return redirect(book.link())
        except Book.DoesNotExist:
            raise Http404


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadIsAuthenticatedOnly)

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)
        return serializer.instance

    def create(self, request, *args, **kwargs):
        write_serializer = BookCreateSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(write_serializer)
        read_serializer = BookListSerializer(instance)

        return Response(read_serializer.data)


class CoverViewset(viewsets.ModelViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'head', 'put']


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.none()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadIsAuthenticatedOnly)

    def get_queryset(self):
        queryset = Review.objects.none()
        book_id = self.request.query_params.get('book_id', None)
        if book_id is not None:
            queryset = Review.objects.filter(book_id=book_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
