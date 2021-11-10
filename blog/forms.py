from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.models import User

from authentication.models import UserProfile
from blog.models import Publication


class CreatePublicationForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), )

    class Meta:
        model = Publication
        fields = ['topic', 'title', 'image', 'short_description', 'description', 'status']


