from django import forms
from django.contrib.auth.models import User
from italiansushi.models import LoginProfile, ItemSet
from jsonfield import JSONField

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # repassword = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    usernameoremail = forms.CharField()

class FileForm(forms.Form):
    json = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

# class ItemForm(forms.Form):
#     json = JSONField()
    
#     class Meta:
#         model = ItemSet
#         fields = ('json',)
#         exclude = ('users',)