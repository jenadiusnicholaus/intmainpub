import django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User

from authentication.forms import UserSignUpForm
from .forms import usersForm, singleUserProfileForm
from blog.models import Publication, Topics
from django.core.paginator import Paginator


def SignUpView(request, ):
    return render(request, template_name='account/signUpModal.html')


def validate_username(request):
    """Check username availability"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def author_page(request, username, pk):
    author_data = User.objects.get(pk=pk)
    publication = Publication.objects.filter(author_id=pk)
    paginator = Paginator(publication, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    topics = Topics.objects.all()

    context = {
        'author_data': author_data,
        'author_publication': publication,
        'page_obj': page_obj,
        'topics': topics
    }
    return render(request, template_name='author_page.html', context=context)


class Register(View):
    def get(self, *args, **kwargs):
        form = UserSignUpForm()
        return render(self.request, 'register.html', {'register_form': form})

    def post(self, request, *args, **kwargs):
        # try:
        form = UserSignUpForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            # cheking for passwords matching
            if password != password2:
                messages.warning(self.request, "password doesn't match")
                # For this we need toredirect to register page if there
                return redirect('register')

            if not (User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists()):
                User.objects.create_user(
                   username, email, password=password,  is_active=True)
                # it going to be used later in the email sending
                user = User.objects.get(username=username, email=email)
                # TODO send email address to activate a user if you want it to
                messages.success(
                    self.request, f'Registered successfully now')
                return redirect('login')
            else:
                messages.warning(
                    self.request, 'Looks like a username with that email or password already exists')
                return redirect("register")
        else:
            # For this we need toredirect to register page if there
            print('from not valid')
            print(form.data)
            messages.warning(self.request, 'Form not valid')
        return redirect('/')
        # except:
        #     return render(request, "error_page.html")


def login_request(request):
    try:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(
                        request, f"You are now logged in as {username}.")
                    return redirect("/")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="login_page.html", context={"login_form": form})
    except:
        return render(request, "error_page.html")


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


class userProfile(View):
    def get(self, request, *args, **kwargs):
        # author_data = User.objects.get(pk=request.user)
        publication = Publication.objects.filter(author=request.user)
        paginator = Paginator(publication, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        topics = Topics.objects.all()

        update_form_user = usersForm(instance=self.request.user)
        update_form_user_profile = singleUserProfileForm(
            instance=self.request.user.userprofile)
        context = {
            # 'author_data': author_data,
            'author_publication': publication,
            'page_obj': page_obj,
            'topics': topics,
            'user_form': update_form_user,
            'profile_form': update_form_user_profile
        }

        return render(request, template_name="userprofile.html", context=context)

    def post(self, request, *args, **kwargs):
        try:
            update_form_user = usersForm(
                self.request.POST or None,
                instance=self.request.user)
            update_form_user_profile = singleUserProfileForm(
                self.request.POST or None, self.request.FILES or None,
                instance=self.request.user.userprofile)
            if update_form_user.is_valid() and update_form_user_profile.is_valid():
                user = update_form_user.save(True)
                profile = update_form_user_profile.save(False)
                profile.user = user
                profile.save()
                messages.success(
                    self.request, ' your profile has been updated successfully')
                return redirect('userprofile')
            else:
                messages.warning(self.request, 'form is invalid')
                print(update_form_user.data, update_form_user_profile.data)
                return redirect('userprofile')

        except ObjectDoesNotExist:
            messages.info(
                self.request, 'Invalid user profile, try to register as a new user.')
            return redirect('userprofile')
