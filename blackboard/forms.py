from django import forms
from tinymce.widgets import TinyMCE


class Answerform(forms.Form):
    answer = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 5}))
