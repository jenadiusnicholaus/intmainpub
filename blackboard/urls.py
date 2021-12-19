from django.urls import path
from . import views

urlpatterns = [
    path('blackboard/', views.blackboard, name="blackboard")
]
