from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('add/', views.post_add, name='post_add'),

]