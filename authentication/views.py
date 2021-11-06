from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import render, redirect
from django.views import View

from authentication.forms import UserSignUpForm
from blog.models import Publication

User = get_user_model()


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

    print(publication.count)
    context = {
        'author_data': author_data,
        'author_publication': publication

    }
    return render(request, template_name='author_page.html', context=context)


class Register(View):
    def get(self, *args, **kwargs):
        form =  UserSignUpForm()
        return render(self.request, 'register.html', {'register_form': form})

    def post(self, request, *args, **kwargs):
        form = UserSignUpForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')


            # print(username)
            # print(email)
            # print(password)
            # print(mobile)

            # cheking for passwords matching
            if password != password2:
                messages.warning(self.request, "password doesn't match")
                # For this we need toredirect to register page if there
                return redirect('register')

            if not (User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists()):
                User.objects.create_user(email, password, username=username, is_active=True)
                # it going to be used later in the email sending
                user = User.objects.get(username=username, email=email)
                # TODO send email address to activate a user if you want it to
                messages.success(self.request, f'Registered successfully now')
                return redirect('login')
            else:
                messages.warning(self.request, 'Looks like a username with that email or password already exists')
                return redirect("register")
        else:
            # For this we need toredirect to register page if there
            print('from not valid')
            print(form.data)
            messages.warning(self.request, 'Form not valid')
        return redirect('/')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login_page.html", context={"login_form": form})


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
