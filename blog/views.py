from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views import View


from .models import *
User = get_user_model()

def home(request):
    publications = Publication.objects.filter(status=1)
    recent = Publication.objects.first()
    recent_posted_pub = Publication.objects.all()[:3]
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

        context = {
            'recent_posted_pub': recent_posted_pub,
            'popular_author': popular_author

        }
        return render(request, template_name='create_publication.html', context=context)
