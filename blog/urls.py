from django.urls import  path
from .  import views

urlpatterns =[
    path('',  views.home, name='home',),
    path('publication_details/<slug:slug>',  views.publication_details, name='publication_details',)
]