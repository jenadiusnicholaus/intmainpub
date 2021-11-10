from django.urls import path

from authentication.views import \
    SignUpView, validate_username, \
    author_page, logout_request,\
    login_request, Register , \
    userProfile

urlpatterns = [
    path('signUp', SignUpView, name='signUp'),
    path('validate_username', validate_username, name='validate_username'),
    path('<str:username>/<int:pk>', author_page, name='author_page'),
    path("login", login_request, name="login"),
    path("register", Register.as_view(), name="register"),
    path("logout", logout_request, name="logout"),
    path("userprofile", userProfile.as_view(), name="userprofile"),

]
