from django import template
from apps.books.models import ReadBook
register = template.Library()


@register.simple_tag
def is_read(book, user):
    if user.is_authenticated:
        try:
            instance = ReadBook.objects.filter(book=book, user=user).last()
            if instance is not None:
                return True
        except ReadBook.DoesNotExist:
            return False


@register.simple_tag
def is_publisher(book, user):
    return book.publisher == user
