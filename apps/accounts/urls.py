from django.conf.urls import url
from apps.accounts.views import *

app_name = 'accounts'
urlpatterns = [
    url(r'^sign-in$', SigninView.as_view(), name='signin'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^lost-password', LostPasswordView.as_view(), name='lost_password'),
    url(r'^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        ResetPasswordView.as_view(), name='reset_password'),
    url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', confirm_email,
        name='confirm_email'),
    url(r'^logout$', sign_out, name='logout'),
]