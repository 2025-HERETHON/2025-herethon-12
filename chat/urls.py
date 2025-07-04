from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 받은 신청에서 "쪽지하기" 누르면 쪽지방 생성 (거래 종류와 id 기반)
    path('start/<str:request_type>/<int:request_id>/', views.start_chat, name='start_chat'),

    # 쪽지방 목록
    path('threads/', views.thread_list, name='thread_list'),
    
    # 특정 쪽지방 입장 (상세 채팅방)
    path('<int:thread_id>/', views.chat_room, name='chat_room'),
    
    # 채팅 메시지 전송
    path('<int:thread_id>/send/', views.send_message, name='send_message'),
    
    # 거래 완료 버튼 클릭 시 거래 완료 처리
    path('<int:thread_id>/complete/', views.complete_trade, name='complete_trade'),
]

# 미디어 파일 처리를 위한 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)