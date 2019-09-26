from django.conf.urls import url
from apps.books.views import *

app_name = 'books'
urlpatterns = [
    url(r'^add$', BookAdd.as_view(), name='add'),
    url(r'^my$', MyBookList.as_view(), name='my'),
    url(r'^(?P<book_id>[0-9]+)$', BookView.as_view(), name='item'),
    url(r'^(?P<book_id>[0-9]+)/mark-as-read$', ReadBookView.as_view(), name='read'),
    url(r'^(?P<book_id>[0-9]+)/edit$', BookEdit.as_view(), name='edit'),
    url(r'^(?P<book_id>[0-9]+)/delete$', BookDelete.as_view(), name='delete'),
]