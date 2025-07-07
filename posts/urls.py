from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('add/', views.post_add, name='post_add'),
    path('<int:item_id>/', views.post_detail, name='post_detail'),
    path('<int:item_id>/delete', views.post_delete, name='post_delete'),
]