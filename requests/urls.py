from django.urls import path
from . import views

app_name = 'requests'  # 템플릿이나 reverse 함수에서 네임스페이스로 사용 가능

urlpatterns = [
    path('donation/received/', views.received_donation_requests, name='received_donation_requests'),
    path('donation/sent/', views.sent_donation_requests, name='sent_donation_requests'),
    
    # 받은 신청 거절 처리
    path('donation/reject/<int:request_id>/', views.reject_donation_request, name='reject_donation_request'),

    # 보낸 신청 관련 (신청 취소/삭제)
    path('donation/sent/<int:request_id>/<str:action>/', views.manage_sent_donation_request, name='manage_sent_donation_request'),

    path('exchange/received/', views.received_exchange_requests, name='received_exchange_requests'),
    path('exchange/sent/', views.sent_exchange_requests, name='sent_exchange_requests'),
    path('exchange/reject/<int:request_id>/', views.reject_exchange_request, name='reject_exchange_request'),
    path('exchange/sent/<int:request_id>/<str:action>/', views.manage_sent_exchange_request, name='manage_sent_exchange_request'),

    path('mypage/exchanges/', views.my_exchange_history, name='my_exchange_history'),
    path('mypage/donations/sent', views.my_sent_donations, name='my_sent_donations'),
    path('mypage/donations/received', views.my_received_donations, name='my_received_donations'),

]