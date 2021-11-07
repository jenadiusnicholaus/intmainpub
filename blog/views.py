from django.shortcuts import render, get_object_or_404
from .models import *


def home(request):
    publications = Publication.objects.filter(status=1)
    recent = Publication.objects.first()
    recent_posted_pub = Publication.objects.all()[:3]
    context = {
        'publications': publications,
        'recent': recent,
        'recent_posted_pub': recent_posted_pub
    }
    return render(request, template_name='homepage.html', context=context)


def publication_details(request, slug):
    publication = Publication.objects.get(slug=slug)
    context = {
        'publication_detail': publication

    }
    return render(request, template_name='publication_details.html', context=context)
