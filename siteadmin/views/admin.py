from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


# Create your models here.


# ---------- login ----------#
class AdminLogin(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(AdminLogin, self).__init__(*args, **kwargs)
