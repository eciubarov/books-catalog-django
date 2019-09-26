from rest_framework import routers
from apps.books.views import BookViewset, AuthorViewset, CategoryViewset, ReviewViewset, CoverViewset

router = routers.DefaultRouter()
router.register(r'books', BookViewset)
router.register(r'authors', AuthorViewset)
router.register(r'categories', CategoryViewset)
router.register(r'reviews', ReviewViewset)
router.register(r'covers', CoverViewset)