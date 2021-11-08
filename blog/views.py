from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .forms import CreatePublicationForm
from .models import *

User = get_user_model()


def home(request):
    publications = Publication.objects.filter(status=1)
    recent = Publication.objects.filter(status=1).first()
    recent_posted_pub = Publication.objects.filter(status=1)[:3]
    topics = Topics.objects.all()
    popular_author = User.objects.all()[:3]
    context = {
        'publications': publications,
        'recent': recent,
        'recent_posted_pub': recent_posted_pub,
        'topics': topics,
        'popular_author': popular_author
    }

    return render(request, template_name='homepage.html', context=context)


def publication_details(request, slug):
    publication = Publication.objects.get(slug=slug)
    topics = Topics.objects.all()
    context = {
        'publication_detail': publication,
        'topics': topics
    }
    return render(request, template_name='publication_details.html', context=context)


class CreatePublication(View):
    def get(self, request, *args, **kwargs):
        recent_posted_pub = Publication.objects.all()[:3]
        popular_author = User.objects.all()[:4]
        form = CreatePublicationForm()

        context = {
            'recent_posted_pub': recent_posted_pub,
            'popular_author': popular_author,
            'form': form,

        }
        return render(request, template_name='create_publication.html', context=context)

    def post(self, request, *args, **kwargs):
        form = CreatePublicationForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            slug = slugify(title)
            topic = form.cleaned_data.get('topic')
            author = request.user
            image = form.cleaned_data.get('image')
            short_description = form.cleaned_data.get('short_description')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')

            publication = Publication()
            publication.topic = topic
            publication.title = title
            publication.author = author
            publication.description = description
            publication.short_description = short_description
            publication.image = image
            publication.status = status
            publication.save()
            messages.info(request, 'Three credits remain in your account.')
            return redirect('/')
        form = CreatePublicationForm()
        context = {
            'form': form,
        }
        return render(request, template_name='create_publication.html', context=context)
