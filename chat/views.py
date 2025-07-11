from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Max
from django.utils.timezone import localtime
from .models import Thread, Message, ThreadReadStatus
from requests.models import DonationRequest, ExchangeRequest
from requests.enums import Status
from .forms import MessageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from collections import defaultdict
from django.utils.timezone import now

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

    # 로그인한 사용자가 관련된 모든 쪽지방 조회
    threads = Thread.objects.filter(
        Q(donation__member=member) | Q(donation__item__member=member) |
        Q(exchange__member=member) | Q(exchange__item__member=member)
    ).annotate(last_msg_time=Max("messages__sent_at")).order_by('-last_msg_time')

    thread_data = []
    for thread in threads:
        # 마지막 읽은 시간 (DB 기반)
        read_status = ThreadReadStatus.objects.filter(thread=thread, member=member).first()
        last_read = read_status.last_read_at if read_status else None

        # 안읽은 메시지 여부 판단
        unread = thread.last_msg_time and (not last_read or thread.last_msg_time > last_read)

        # 상대방 프로필 사진
        opponent = thread.get_opponent(member)
        opponent_image = opponent.image.url if opponent and opponent.image else None

        thread_data.append((thread, unread, opponent_image))

    return render(request, 'chat/chat_list.html', {
        'threads': thread_data,
        'current_user': request.user,
    })


# 3. 쪽지방 상세 채팅 화면
@login_required
def chat_room(request, thread_id):
    # 쪽지방 불러오기
    thread = get_object_or_404(Thread, pk=thread_id)
    messages = thread.messages.all().order_by('sent_at')

    # 기본 이동 URL (뒤로가기 대비용)
    redirect_url = reverse('chat:thread_list')

    # 날짜별 메시지 묶기
    grouped = defaultdict(list)
    for msg in messages:
        date = localtime(msg.sent_at).strftime("%Y.%m.%d")
        grouped[date].append(msg)

    # 읽음 시간 DB에 저장 (ThreadReadStatus 기반)
    last_msg = messages.last()
    if last_msg:
        ThreadReadStatus.objects.update_or_create(
            thread=thread,
            member=request.user,
            defaults={'last_read_at': now()}
        )

    # 거래 상태 및 사용자 역할 판단
    is_completed = False
    is_receiver = False
    status = None

    if thread.donation:
        donation = thread.donation
        status = donation.status  # 'WAITING', 'IN_PROGRESS', ...
        is_completed = donation.status == Status.COMPLETED
        is_receiver = donation.item.member == request.user

    elif thread.exchange:
        exchange = thread.exchange
        status = exchange.status
        is_completed = exchange.status == Status.COMPLETED
        is_receiver = exchange.item.member == request.user

    # 템플릿 렌더링
    context = {
        'thread': thread,
        'grouped_messages': dict(grouped),
        'redirect_url': redirect_url,
        'is_completed': is_completed,
        'is_receiver': is_receiver,
        'status': status,  # 템플릿에서 WAITING / IN_PROGRESS / COMPLETED 판단용
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
            
            # 메시지 저장 이후 상태 변경 처리
            if thread.donation:
                donation_request = thread.donation
                if donation_request.status == Status.WAITING.value:
                    donation_request.status = Status.IN_PROGRESS.value
                    donation_request.save()
            elif thread.exchange:
                exchange_request = thread.exchange
                if exchange_request.status == Status.WAITING.value:
                    exchange_request.status = Status.IN_PROGRESS.value
                    exchange_request.save()

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

        donation_request.item.status = Status.COMPLETED  # 아이템 상태도 변경
        donation_request.item.save()

        # 내가 선택하지 않은 다른 신청자들은 모두 거절 처리
        DonationRequest.objects.filter(item=donation_request.item).exclude(pk=donation_request.pk).update(status=Status.REJECTED)

    elif thread.exchange:
        exchange_request = thread.exchange
        if exchange_request.item.member != request.user and exchange_request.member != request.user:
            return redirect('chat:chat_room', thread_id=thread_id)

        # 상태 변경
        exchange_request.status = Status.COMPLETED
        exchange_request.save()

        exchange_request.item.status = Status.COMPLETED  # 아이템 상태도 변경
        exchange_request.item.save()

        # 내가 선택하지 않은 다른 신청자들은 모두 거절 처리
        ExchangeRequest.objects.filter(item=exchange_request.item).exclude(pk=exchange_request.pk).update(status=Status.REJECTED)

    return redirect('chat:chat_room', thread_id=thread_id)