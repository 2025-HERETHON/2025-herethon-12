from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('add/', views.post_add, name='post_add'),
    path('<int:item_id>/', views.post_detail, name='post_detail'),
    path('<int:item_id>/delete', views.post_delete, name='post_delete'),
    path('<int:item_id>/update', views.post_update, name='post_update'),
    path('<int:item_id>/exchange/', views.exchange_request, name='exchange_request'),
    path('<int:item_id>/donation/', views.donation_request, name='donation_request'),
]