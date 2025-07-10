from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('write/<str:request_type>/<int:request_id>/', views.create_review, name='create_review'),
    path('test/', TemplateView.as_view(template_name='reviews/review_post.html'), name='review_test'),
    #path('my/', views.my_review_view, name='my_reviews'),
    #path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('mypage/', views.my_page, name='my_page'),
    path('mypage/edit/', views.edit_profile, name='edit_profile'),
    path('mypage/check-id/', views.check_id_duplicate, name='check_id_duplicate'),

    path('mypage/exchanges/', views.my_exchange_history, name='my_exchange_history'),
    path('mypage/donations/sent', views.my_sent_donations, name='my_sent_donations'),
    path('mypage/donations/received', views.my_received_donations, name='my_received_donations'),

    path('mypage/reviews/', views.my_reviews_view, name='my_reviews_view'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]