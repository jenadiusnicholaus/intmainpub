from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name='home',),
    path('publication_details/<slug:slug>',
         views.PublicationDetails.as_view(), name='publication_details',),
    path('create_publication/',  views.CreatePublication.as_view(),
         name='create_publication'),
    # ajax-posting / name = that we will use in ajax url
    path('ajax-commenting/<slug>', views.ajax_commenting, name='ajax_commenting'),
    path('get_comment/<slug:slug>', views.get_comment, name="get_comment"),
    path('ajax_replying/<int:pk>', views.ajax_replying, name="ajax_replying"),
    path('search/', views.publication_search, name='search'),
    path('topic_items/<pk>', views.topics_details, name="topic_items"),
    path('edit_publication/<pk>', views.edit_publication, name="edit_publication"),



]
