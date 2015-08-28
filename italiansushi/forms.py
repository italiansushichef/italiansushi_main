from django import forms
from django.contrib.auth.models import User
from italiansushi.models import *
from jsonfield import JSONField

# for creating new users
class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # repassword = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# for creating new users
class CreateUserSaveForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # repassword = forms.CharField(widget=forms.PasswordInput())
    idToSave = forms.IntegerField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# for logging in
class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    usernameoremail = forms.CharField()

# for logging in and saving
class LoginSaveForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    usernameoremail = forms.CharField()
    idToSave = forms.IntegerField()

# For uploading items
class FileForm(forms.Form):
    champ1 = forms.CharField(max_length=32, required=False)
    champ2 = forms.CharField(max_length=32, required=False)
    lane = forms.CharField(max_length=1, required=False)
    json = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

# For deleting items
class DeleteItemSetForm(forms.Form):
    name = forms.CharField(max_length=32)
    user = forms.CharField(max_length=None)

# For generating itemsets
class GenerateItemSetForm(forms.Form):
    champ1 = forms.CharField(max_length=128, required=False)
    champ2 = forms.CharField(max_length=128, required=False)
    lane = forms.CharField(max_length=16, required=False)

# For saving items to your profile
class SaveItemSetForm(forms.Form):
    idToSave = forms.IntegerField()
