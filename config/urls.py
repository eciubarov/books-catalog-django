from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView
from apps.books.views import BookList
from .api import router


urlpatterns = [
    url(r'^$', BookList.as_view(), name='home'),
    url(r'^privacy/$',
        TemplateView.as_view(template_name='pages/privacy.html'), name='privacy'),

    # Users management
    url(r'^users/', include('apps.accounts.urls', namespace='users')),
    url(r'^books/', include('apps.books.urls', namespace='books')),
    path('api/', include(router.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
