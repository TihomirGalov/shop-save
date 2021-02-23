from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ), required=False)
    guest_login = forms.CharField(required=False)

    def clean(self):
        if len(self.cleaned_data.get('guest_login')):
            username = 'guest'
            password = 'guest'
        else:
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise self.get_invalid_login_error()
        else:
            self.confirm_login_allowed(self.user_cache)

        return {'username': username, 'password': password}
