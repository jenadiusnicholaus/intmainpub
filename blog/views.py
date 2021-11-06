from django.shortcuts import render, get_object_or_404
from .models import *


def home(request):
    publications = Publication.objects.all()
    context = {
        'publications': publications
    }
    return render(request, template_name='homepage.html', context=context)


def publication_details(request, slug):
    publication = Publication.objects.get(slug=slug)
    context = {
        'publication_detail': publication
    }
    return render(request, template_name='publication_details.html', context=context)

