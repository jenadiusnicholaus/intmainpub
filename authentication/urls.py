from django.urls import path

from authentication.views import \
    SignUpView, validate_username, \
    author_page, logout_request,\
    login_request, Register, \
    userProfile, follow_unfollow, \
    get_follow_following

urlpatterns = [
    path('signUp', SignUpView, name='signUp'),
    path('validate_username', validate_username, name='validate_username'),
    path('<str:username>/<int:pk>', author_page, name='author_page'),
    path("login", login_request, name="login"),
    path("register", Register.as_view(), name="register"),
    path("logout", logout_request, name="logout"),
    path("userprofile", userProfile.as_view(), name="userprofile"),
    path('follow/<username>', follow_unfollow, name="follow_unfollow"),
    path("get_follow_following/<username>", get_follow_following,
         name="get_follow_following")

]
