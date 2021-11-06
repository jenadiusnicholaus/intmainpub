from django.urls import path

from authentication.views import SignUpView, validate_username, author_page

urlpatterns = [
    path('signUp', SignUpView, name='signUp'),
    path('validate_username', validate_username, name='validate_username'),
    path('<str:username>/', author_page, name='author_page')
]
