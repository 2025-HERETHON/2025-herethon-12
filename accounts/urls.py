from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.login_page, name='login'), #로그인
    path('signup/', views.signup_page, name='signup'), #회원가입
    path('logout/', views.user_logout, name='logout'), #로그아웃
    path('location/', views.my_region, name='location'),
    path('profile/<int:pk>/', views.profile_view, name='profile'), #다른 사람 프로필
    path('test/', TemplateView.as_view(template_name='home/profile.html')),
]