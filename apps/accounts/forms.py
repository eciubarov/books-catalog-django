import datetime
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    placeholders = {
        'username': _('Your username'),
        'email': _('Your email'),
        'password': _('Password'),
        'repeat_password': _('Repeat password')
    }

    username = forms.CharField(max_length=64, label=_("Username"))
    email = forms.EmailField(max_length=64, label=_("Email"))
    repeat_password = forms.CharField(widget=forms.PasswordInput,  label=_('Password again'))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        labels = {
            'password': _('Password'),
        }

        widgets = {
            'password': forms.PasswordInput
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages['required'] = _('This field is required.')
            self.fields[field].widget.attrs.update({
                'placeholder': self.placeholders[field]
            })

    def clean_repeat_password(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
            raise forms.ValidationError(_("Passwords do not match."))

    def save(self, commit=True):
        _user = super(SignUpForm, self).save(commit=False)
        _user.set_password(self.cleaned_data["password"])
        _user.is_active = False
        _user.email = self.cleaned_data['email']

        if commit:
            _user.save()

        return _user


class SignInForm(forms.Form):
    placeholders = {
        'username': _('Your username'),
        'password': _('Enter password')
    }

    username = forms.CharField(label=_('Email'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))

    class Meta:
        labels = {
            'username': _('Username'),
            'password': _('Enter password'),
        }

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages['required'] = _('This field is required.')
            self.fields[field].widget.attrs.update({
                'placeholder': self.placeholders[field]
            })

    def clean(self):
        if not authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password')):
            raise forms.ValidationError({'password': [_('Incorrect login or password.')]})


class LostPasswordForm(forms.Form):
    placeholders = {
        'email': _('Email')
    }

    email = forms.EmailField(label='')

    class Meta:
        labels = {
            'email': _('Электронный адрес')
        }

    def __init__(self, *args, **kwargs):
        super(LostPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages['required'] = _('Please write your email address.')
            self.fields[field].widget.attrs.update({
                'placeholder': self.placeholders[field]
            })

    def clean(self):
        try:
            user = User.objects.get(email=self.cleaned_data.get('email'))
        except:
            raise forms.ValidationError({'email': [_('This email address is not registered.')]})


class ResetPasswordForm(forms.Form):
    placeholders = {
        'password': _('New password'),
        'repeat_password': _('Repeat new password'),
    }

    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': self.placeholders[field]
            })

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
            raise forms.ValidationError(_('The passwords you entered do not match.'))