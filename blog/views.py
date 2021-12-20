from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.serializers import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from hitcount.views import HitCountDetailView
import json
from django.db.models import Q
import datetime


from .forms import PublicationForm
from .models import *


def home(request):
    try:

        publications = Publication.objects.filter(status=1)
        recent = Publication.objects.filter(status=1).first()
        recent_posted_pub = Publication.objects.filter(status=1)[:3]
        topics = Topics.objects.all()
        popular_author = []
        author = Publication.objects.select_related('author').all()[:4]
        for auth in author:
            if auth.author not in popular_author:
                popular_author.append(auth.author)

        paginator = Paginator(publications, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'publications': publications,
            'recent': recent,
            'recent_posted_pub': recent_posted_pub,
            'topics': topics,
            'popular_author': popular_author,
            'page_obj': page_obj
        }

        return render(request, template_name='homepage.html', context=context)

    except:
        return render(request, template_name='error_page.html')


class PublicationDetails(HitCountDetailView):
    model = Publication
    template_name = 'publication_details.html'
    context_object_name = 'publication_detail'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        try:
            context = super(PublicationDetails,
                            self).get_context_data(**kwargs)
            topics = Topics.objects.all()
            recent_posted_pub = Publication.objects.filter(status=1)[:3]

            context.update({
                'recent_posted_pub': recent_posted_pub,

                'popular_posts': Publication.objects.order_by('-hit_count_generic__hits')[:3],
                'topics': topics
            })
            return context
        except:
            return render(self.request, template_name='error_page.html')


class CreatePublication(View):
    def get(self, request, *args, **kwargs):
        try:
            recent_posted_pub = Publication.objects.all()[:3]
            popular_author = User.objects.all()[:4]
            form = PublicationForm()
            topic = Topics.objects.all()

            context = {
                'recent_posted_pub': recent_posted_pub,
                'popular_author': popular_author,
                'form': form,
                'topics': topic
            }

            return render(request, template_name='create_publication.html', context=context)
        except:
            return render(request, template_name='error_page.html')

    def post(self, request, *args, **kwargs):
        try:
            form = PublicationForm(request.POST, request.FILES)
            if request.user.is_authenticated:
                if form.is_valid():
                    title = form.cleaned_data.get('title')
                    slug = slugify(title)
                    topic = form.cleaned_data.get('topic')
                    author = request.user
                    image = form.cleaned_data.get('image')
                    short_description = form.cleaned_data.get(
                        'short_description')
                    description = form.cleaned_data.get('description')
                    status = form.cleaned_data.get('status')
                    bitBucket_link = form.cleaned_data.get("bitBucket_link")
                    docker_link = form.cleaned_data.get("docker_link")
                    gitlab_link = form.cleaned_data.get("gitlab_link")
                    github_link = form.cleaned_data.get("github_link")

                    publication = Publication()
                    publication.topic = topic
                    publication.title = title
                    publication.author = author
                    publication.description = description
                    publication.short_description = short_description
                    publication.image = image
                    publication.status = status
                    publication.bitBucket_link = bitBucket_link
                    publication.docker_link = docker_link
                    publication.gitlab_link = gitlab_link
                    publication.github_link = github_link
                    publication.save()
                    messages.info(request, 'Publication was created success.')
                    return redirect('/')
                else:
                    print(form.is_valid(), )
                    context = {
                        # 'form': form,
                    }
                    messages.info(
                        request, 'Login to continue')

                    return redirect('create_publication')
            else:
                return redirect('login')

        except:
            return render(request, template_name='error_page.html')


def get_comment(request, slug):
    pub = Publication.objects.get(slug=slug)
    comments = PublicationComment.objects.filter(
        publication=pub).order_by('-created_on')
    html = ''
    comment_counter = comments.count()

    for i in comments:
        created_on = i.created_on.strftime("%d %b %Y")
        if i.commenter.userprofile.imageUrl():
            image = ' <img style ="width: 50px; height:50px;" class="avatar-img rounded-circle border border-3 border-dark mr-5"  src='f"{i.commenter.userprofile.imageUrl()}"'  alt="avatar">'
        else:
            image = '<div class="avatar mr-5">' + '<div style ="width: 50px; height:50px;" class="avatar-img rounded-circle bg-primary"><span class="text-white position-absolute top-50 start-50 translate-middle fw-bold">' + \
                f'{i.commenter.userprofile.getfirstChar()}' + \
                ' </span></div>' + '</div>'

        el = '<div class="my-4 d-flex ps-2 ps-md-3">' + f'{image}' + '<div>' + '<div class="mb-2">' + '<h5 class="m-3">' + f'{i.commenter.userprofile.get_fullname()}' + '</h5>' + '<span class="me-3 small">' + \
            f'Commented on {created_on}' + '</span>' + '<a href="#" class="text-body fw-normal"></a>' + \
            '</div>' + '<p>' + f'{i.content}' + '</p>' + '</div>' + '</div>'

        ele = '<div> <article>  <p> <span> Author:' + f'{i.commenter.username}' + '</span > </p > <p>' + i.content +\
              '<ul> <li> <a href = "rel external nofollow > </a> </li> </ul> </article > </div HR'
        html += el
    return HttpResponse(json.dumps({'comment': html, 'counter': comment_counter}))


def ajax_commenting(request, slug):
    try:
        if request.is_ajax():
            publication = Publication.objects.get(slug=slug)

            # getting data from first_name input
            comment = request.POST.get('comment', None)
            print(comment)
            if comment:  # cheking if first_name and last_name have value
                user = request.user
                PublicationComment.objects.create(
                    content=comment,
                    publication=publication,
                    commenter=user)
                response = {
                    'msg': 'successfully'  # response message
                }
                return JsonResponse(response)  # return response as JSON
    except:
        return render(request, template_name='error_page.html')


def ajax_replying(request, pk):
    response = {
        'msg': 'successfully'  # response message
    }
    return JsonResponse(response)  # return response as JSON


def get_replying(request, pk):
    response = {
        'msg': 'successfully'  # response message
    }
    return JsonResponse(response)  # return response as JSON


def publication_search(request):
    try:
        if request.method == 'GET':
            query = request.GET.get('q')

            pub_submitted = request.GET.get('submit')

            if query is not None:
                lookups = Q(title__icontains=query) | Q(title__icontains=query)

                results = Publication.objects.filter(lookups).distinct()
                topics = Topics.objects.all()

                context = {
                    'results': results,
                    'topics': topics,
                    'submitbutton': pub_submitted}

                return render(request, 'search.html', context)

            else:
                topics = Topics.objects.all()
                context = {
                    'topics': topics
                }
                return render(request, 'search.html', context=context)

        else:
            return render(request, 'search.html')
    except:
        return render(request, template_name='error_page.html')


def topics_details(request, pk):
    # try:
    topic = Topics.objects.get(id=pk)
    topics = Topics.objects.all()[:5]

    pubs = Publication.objects.filter(topic_id=pk)
    paginator = Paginator(pubs, 20)
    count_pubs = pubs.count()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'topics': topics,
        'topic': topic,
        'page_obj': page_obj,
        'count_pubs': count_pubs,

    }
    return render(request, 'topic_items.html', context=context)
    # except:
    #     return render(request, template_name='error_page.html')


def edit_publication(request, pk):
    recent_posted_pub = Publication.objects.filter(status=1)[:3]
    obj = Publication.objects.get(id=pk)
    if request.method == 'POST':
        form = PublicationForm(
            request.POST, request.FILES or None, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(
                request, f'{obj.title} has been edited successfully')
            return redirect('edit_publication',  pk=obj.pk)

        # return render(request, 'edit_publication.html', context={'form': form})
    else:
        form = PublicationForm(instance=obj)
        popular_author = User.objects.all()[:4]
        context = {
            'recent_posted_pub': recent_posted_pub,
            'form': form,
            'popular_author': popular_author,

        }

        return render(request, 'edit_publication.html', context=context)
