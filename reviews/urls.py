from django.urls import path
from . import views

urlpatterns = [
    path('write/<str:request_type>/<int:request_id>/', views.create_review, name='create_review'),
    path('my/', views.my_review_view, name='my_reviews'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]