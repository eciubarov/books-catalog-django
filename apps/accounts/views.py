from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from .tasks import *
from .mixins import AnonymousMixin
from .forms import SignUpForm, SignInForm, LostPasswordForm, ResetPasswordForm


class SigninView(AnonymousMixin, View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'accounts/signin.html', locals())

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            _user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if _user is not None:
                login(request, _user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect(reverse('home'))
        else:
            return render(request, 'accounts/signin.html', locals())


class SignupView(AnonymousMixin, View):
    success = False

    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', locals())

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            success = True

            token = default_token_generator.make_token(f)
            uid = urlsafe_base64_encode(force_bytes(f.pk))
            title = 'Account activation at demo-books-django'
            message = render_to_string('emails/signup.html',
                                       {'link': request.build_absolute_uri(reverse('users:confirm_email',
                                                                                   kwargs={'uidb64': uid, 'token': token}))})
            AsyncEmail(f.email,title,message)
        return render(request, 'accounts/signup.html', locals())


class LostPasswordView(AnonymousMixin, View):

    def get(self, request):
        success = False
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        form = LostPasswordForm()
        return render(request, 'accounts/lost-password.html', locals())

    def post(self, request):
        form = LostPasswordForm(request.POST)
        success = False
        if form.is_valid():
            success = True
            user = User.objects.get(email=form.cleaned_data.get('email'))
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            title = 'Reset password at demo-books-django'
            message = render_to_string('emails/reset-password.html', {
                'email': user.email, 'link': request.build_absolute_uri(reverse('users:reset_password',
                                                                                kwargs={'uidb64': uid, 'token': token}))})
            AsyncEmail(user.email,title,message)
        return render(request, 'accounts/lost-password.html', locals())


class ResetPasswordView(AnonymousMixin, View):

    def get(self, request, uidb64, token):
        success = False
        form = ResetPasswordForm()
        return render(request, 'accounts/reset-password.html', locals())

    def post(self, request, uidb64, token):
        success = False
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            if uidb64 is not None and token is not None:
                uid = urlsafe_base64_decode(uidb64)
                try:
                    user_model = get_user_model()
                    user = user_model.objects.get(pk=uid)
                    if default_token_generator.check_token(user, token):
                        print(form.cleaned_data.get('password'))
                        user.set_password(form.cleaned_data.get('password'))
                        user.save()
                        success = True
                        return redirect(reverse('users:signin'))
                except:
                    return HttpResponse('Activation link is invalid!')
        return render(request, 'accounts/reset-password.html', locals())


def confirm_email(request, uidb64, token):
    if uidb64 is not None and token is not None:
        uid = urlsafe_base64_decode(uidb64)
        try:
            user_model = get_user_model()
            user = user_model.objects.get(pk=uid)
            # print(user)
            if default_token_generator.check_token(user, token) and user.is_active is False:
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(reverse('home'))
            else:
                return HttpResponse('Activation link is invalid!')
        except User.DoesNotExist:
            return HttpResponse('Error!')
    return redirect(reverse('home'))


@login_required
def sign_out(request):
    logout(request)
    return redirect(reverse('users:signin'))