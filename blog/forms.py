from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.models import User
from django.utils.regex_helper import Choice

from authentication.models import UserProfile
from blog.models import STATUS, Publication, Topics


class PublicationForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), )
    bitBucket_link = forms.URLField(max_length=400, required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'bitbucket link'
    }))
    docker_link = forms.URLField(max_length=400, required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Docker image link'
    }))
    gitlab_link = forms.URLField(max_length=400, required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Gitlab link'

    }))
    github_link = forms.URLField(max_length=400,  widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Github link'
    }))

    # [(topic.title, topic.title) for topic in Topics.objects.all()]
    # topic = forms.ChoiceField(
    #     widget=forms.Select(attrs={
    #         'class': 'form-control'
    #     }),)
    status = forms.ChoiceField(
        choices=STATUS, widget=forms.Select(attrs={
            'class': 'form-control'
        }))

    image = forms.ImageField()
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    short_description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 2,
        'cols': 25

    }))

    class Meta:
        model = Publication
        fields = [
            'topic',
            'title',
            'image',
            'short_description',
            'description',
            'status',
            'bitBucket_link',
            'docker_link',
            'gitlab_link',
            'github_link',

        ]
