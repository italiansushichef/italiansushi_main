from django import forms
from django.contrib.auth.models import User
from italiansushi.models import LoginProfile

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # repassword = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    usernameoremail = forms.CharField()
