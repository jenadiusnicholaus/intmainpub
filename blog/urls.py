from django.urls import  path
from .  import views

urlpatterns =[
    path('',  views.home, name='home',),
    path('publication_details/<slug:slug>',  views.PublicationDetails.as_view(), name='publication_details',),
    path('create_publication/',  views.CreatePublication.as_view(), name='create_publication',),
    path('ajax-commenting/<slug>',views.ajax_commenting, name='ajax_commenting'),  # ajax-posting / name = that we will use in ajax url
    path('add_comment/<slug:slug>', views.comment, name = 'add_comment'),
    path('get_comment/<slug:slug>', views.get_comment, name ="get_comment"),
    path('ajax_replying/<int:pk>', views.ajax_replying, name="ajax_replying")

]