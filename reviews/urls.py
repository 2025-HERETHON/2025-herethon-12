from django.urls import path
from . import views

urlpatterns = [
    path('write/<str:request_type>/<int:request_id>/', views.create_review, name='create_review'),
]