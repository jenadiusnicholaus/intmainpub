from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserSignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()
