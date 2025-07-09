from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Max
from django.utils.timezone import localtime
from .models import Thread, Message
from requests.models import DonationRequest, ExchangeRequest
from requests.enums import Status
from .forms import MessageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# 1. 쪽지방 생성
@login_required
def start_chat(request, request_type, request_id):
    if request_type == "donation":
        donation = get_object_or_404(DonationRequest, pk=request_id)
        thread, created = Thread.objects.get_or_create(donation=donation)
        # 신청 관리에서 들어온 경우
        request.session['previous_page'] = reverse('requests:received_donation_requests')
    elif request_type == "exchange":
        exchange = get_object_or_404(ExchangeRequest, pk=request_id)
        thread, created = Thread.objects.get_or_create(exchange=exchange)
        # 교환 신청 관리에서 들어온 경우로 수정 가능
        request.session['previous_page'] = reverse('requests:received_exchange_requests')
    else:
        return redirect('home')

    return redirect('chat:chat_room', thread_id=thread.thread_id)


# 2. 쪽지방 목록 조회
@login_required
def thread_list(request):
    # 쪽지 목록에서 들어온 경우를 세션에 기록
    request.session['previous_page'] = reverse('chat:thread_list')

    member = request.user
    threads = Thread.objects.filter(
        Q(donation__member=member) | Q(donation__item__member=member) |
        Q(exchange__member=member) | Q(exchange__item__member=member)
    ).annotate(last_msg_time=Max("messages__sent_at")).order_by('-last_msg_time')

    return render(request, 'chat/chat_list.html', {'threads': threads})


# 3. 쪽지방 상세 채팅 화면
@login_required
def chat_room(request, thread_id):
    #특정 쪽지방 안의 메시지들을 시간순으로 불러옴
    thread = get_object_or_404(Thread, pk=thread_id)
    messages = thread.messages.all().order_by('sent_at')

    # 이전 페이지 세션 없으면 쪽지 목록으로
    redirect_url = reverse('chat:thread_list')

    # 날짜별로 그룹화하여 전달 ex) 2025.07.04: [msg1, msg2]  
    grouped = {}
    for msg in messages:
        date = localtime(msg.sent_at).strftime("%Y.%m.%d")
        grouped.setdefault(date, []).append(msg)

    context = {
        'thread': thread,
        'grouped_messages': grouped,
        'redirect_url': redirect_url,
    }
    return render(request, 'chat/chat.html', context)


# 4. 메시지 전송
@login_required
def send_message(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False) # 아직 DB에 저장X
            message.thread = thread # 쪽지방 연결
            message.member = request.user # 보낸 사람
            message.save() # 최종 저장
        else:
            messages.error(request, "메시지 전송 중 오류가 발생했습니다.")

    # chat_room으로 다시 이동해 새 메시지가 보이게 됨
    return redirect('chat:chat_room', thread_id=thread_id)

# 5. 거래 완료 처리
@login_required
def complete_trade(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    # 로그인한 유저가 거래 주인인지 확인 (예: 게시물 주인 or 신청자)
    if thread.donation:
        donation_request = thread.donation
        if donation_request.item.member != request.user and donation_request.member != request.user:
            return redirect('chat:chat_room', thread_id=thread_id)

        # 상태 변경
        donation_request.status = Status.COMPLETED
        donation_request.save()

    elif thread.exchange:
        exchange_request = thread.exchange
        if exchange_request.item.member != request.user and exchange_request.member != request.user:
            return redirect('chat:chat_room', thread_id=thread_id)

        # 상태 변경
        exchange_request.status = Status.COMPLETED
        exchange_request.save()

    return redirect('chat:chat_room', thread_id=thread_id)