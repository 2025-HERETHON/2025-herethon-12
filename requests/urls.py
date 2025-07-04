from django.urls import path
from . import views

app_name = 'requests'  # 템플릿이나 reverse 함수에서 네임스페이스로 사용 가능

urlpatterns = [
    path('received/', views.received_donation_requests, name='received_donation_requests'),
    path('sent/', views.sent_donation_requests, name='sent_donation_requests'),
    
    # 받은 신청 거절 처리
    path('reject/<int:request_id>/', views.reject_donation_request, name='reject_donation_request'),

    # 보낸 신청 관련 (신청 취소/삭제)
    path('sent/<int:request_id>/<str:action>/', views.manage_sent_donation_request, name='manage_sent_donation_request'),
]