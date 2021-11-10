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


from .forms import CreatePublicationForm
from .models import *

User = get_user_model()


def home(request):
    try:
        publications = Publication.objects.filter(status=1)
        recent = Publication.objects.filter(status=1).first()
        recent_posted_pub = Publication.objects.filter(status=1)[:3]
        topics = Topics.objects.all()
        popular_author = User.objects.all()[:4]

        # publication pagination

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

        context = super(PublicationDetails, self).get_context_data(**kwargs)
        topics = Topics.objects.all()
        context.update({
            'popular_posts': Publication.objects.order_by('-hit_count_generic__hits')[:3],
            'topics': topics
        })
        return context



class CreatePublication(View):
    def get(self, request, *args, **kwargs):
        try:
            recent_posted_pub = Publication.objects.all()[:3]
            popular_author = User.objects.all()[:4]
            form = CreatePublicationForm()

            context = {
                'recent_posted_pub': recent_posted_pub,
                'popular_author': popular_author,
                'form': form,
            }

            return render(request, template_name='create_publication.html', context=context)
        except :
            return render(request, template_name='error_page.html')

    def post(self, request, *args, **kwargs):
        try:
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
        except :
            return render(request, template_name='error_page.html')




def get_comment(request, slug):
    pub = Publication.objects.get( slug=slug)
    comments = PublicationComment.objects.filter(publication = pub).order_by('-created_on')
    html = ''
    comment_counter = comments.count()

    for i in comments:
        if  i.commenter.userprofile.imageUrl():
            image  = ' <img style ="width: 50px; height:50px;" class="avatar-img rounded-circle border border-3 border-dark mr-5"  src='f"{i.commenter.userprofile.imageUrl()}"'  alt="avatar">'
        else:
            image = '<div class="avatar mr-5">' + '<div style ="width: 50px; height:50px;" class="avatar-img rounded-circle bg-primary"><span class="text-white position-absolute top-50 start-50 translate-middle fw-bold">' + f'{i.commenter.getfirstChar()}' + ' </span></div>' + '</div>'

        el = '<div class="my-4 d-flex ps-2 ps-md-3">' + f'{image}' + '<div>' + '<div class="mb-2">' + '<h5 class="m-3">' + f'{i.commenter.get_fullname()}'+ '</h5>' + '<span class="me-3 small">'+ f'{i.created_on}' + '</span>' + '<a href="#" class="text-body fw-normal"></a>'+ '</div>'+ '<p>' + f'{i.content}' + '</p>'+ '</div>'+ '</div>'

        ele = '<div> <article>  <p> <span> Author:' + f'{i.commenter.username}' + '</span > </p > <p>' + i.content +\
              '<ul> <li> <a href = "rel external nofollow > </a> </li> </ul> </article > </div HR'
        html += el
    return HttpResponse(json.dumps({'comment': html, 'counter': comment_counter}))


def ajax_commenting(request, slug):
    try:
        if request.is_ajax():
            publication = Publication.objects.get(slug = slug)

            comment = request.POST.get('comment', None) # getting data from first_name input
            print(comment)
            if comment: #cheking if first_name and last_name have value
                user = request.user
                PublicationComment.objects.create(
                    content=comment,
                    publication=publication,
                    commenter=user)
                response = {
                    'msg':'successfully' # response message
                }
                return JsonResponse(response) # return response as JSON
    except :
        return render(request, template_name='error_page.html')

def ajax_replying(request, pk):
    response = {
                'msg':'successfully' # response message
            }
    return JsonResponse(response) # return response as JSON

def get_replying(request, pk):
    response = {
               'msg':'successfully' # response message
            }
    return JsonResponse(response) # return response as JSON


def publication_search(request):
    try:
        if request.method == 'GET':
            query = request.GET.get('q')

            pub_submitted = request.GET.get('submit')

            if query is not None:
                lookups = Q(title__icontains=query) | Q( title__icontains=query)

                results = Publication.objects.filter(lookups).distinct()
                topics = Topics.objects.all()

                context = {
                    'results': results,
                    'topics':topics,
                'submitbutton': pub_submitted}

                return render(request, 'search.html', context)

            else:
                topics = Topics.objects.all()
                context ={
                    'topics':topics
                }
                return render(request, 'search.html', context=context)

        else:
            return render(request, 'search.html')
    except :
        return render(request, template_name='error_page.html')

