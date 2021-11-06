from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from intmainblog import settings

User = settings.AUTH_USER_MODEL


def SignUpView(request, ):
    return render(request, template_name='account/signUpModal.html')


def validate_username(request):
    """Check username availability"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def author_page(request, username):
    context = {

    }
    return render(request, template_name='author_page.html', context=context)
