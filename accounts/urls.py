from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', views.signup_page, name='signup'),
]