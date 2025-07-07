from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('location/', TemplateView.as_view(template_name='accounts/location.html')),
    path('mypage/', views.my_page, name='my_page'),
    path('mypage/edit/', views.edit_profile, name='edit_profile'),
    path('mypage/check-id/', views.check_id_duplicate, name='check_id_duplicate'),
]