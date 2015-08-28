from django import forms
from django.contrib.auth.models import User
from italiansushi.models import LoginProfile, ItemSet
from jsonfield import JSONField

# for creating new users
class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # repassword = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# for logging in
class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    usernameoremail = forms.CharField()

# For uploading items
class FileForm(forms.Form):
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
    filenameToSave = forms.CharField(max_length=32)
    idToSave = forms.IntegerField()
