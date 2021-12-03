from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# from django.contrib.auth.models import User

from authentication.models import UserProfile

User = get_user_model()


class UserSignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()


# user form
class usersForm(forms.ModelForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your username here...',
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your email here...',
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your first name here...',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your last name here...',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


# user profile form
class singleUserProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control ',
        'rows': "1",
        'cols': "100",
        'placeholder': 'Write your bio here...',

    }))
    about = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control ',
        'rows': "1",
        'cols': "100",
        'placeholder': 'Write your about here...',

    }))
    profession = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your profession here...',
    }))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Write your location here...',
    }))
    facebook_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your facebook link here...',
    }))

    linkedin_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your linked link here...',
    }))
    tweeter_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your tweeter link here...',
    }))
    github_link = forms.URLField(required=False,  widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Write your github link here...',
    }))
    image = forms.FileField(required=False,  widget=forms.FileInput(attrs={
        'class': 'form-control',

    }))

    class Meta:
        model = UserProfile
        fields = ('image', 'bio', 'profession', 'location', 'about', 'facebook_link', 'linkedin_link', 'tweeter_link',
                  'github_link')
