from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
]