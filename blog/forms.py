from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.models import User

from authentication.models import UserProfile
from blog.models import Publication


class CreatePublicationForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), )
    bitBucket_link = forms.URLField(max_length=400,required = False, widget = forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'bitbucket link'
    }))
    docker_link = forms.URLField(max_length=400,required = False, widget = forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'Docker image link'
    }))
    gitlab_link = forms.URLField(max_length=400,required = False, widget = forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'Gitlab link'

    }))
    github_link = forms.URLField(max_length=400,  widget = forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'Github link'
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
            'gitlab_link',

            ]


