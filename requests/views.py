from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from requests.models import DonationRequest, ExchangeRequest
from posts.models import Item
from requests.enums import Status
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from collections import defaultdict


# ------------------------
# 기존 신청 관련 뷰들
# ------------------------

# 나눔-받은 신청 목록 조회
@login_required
def received_donation_requests(request):
    print("로그인 상태:", request.user.is_authenticated)  # True면 로그인됨
    print("현재 사용자:", request.user.username)

    member = request.user
    my_items = Item.objects.filter(member=member)

    # 거절된(REJECTED) 요청 제외
    donation_requests = DonationRequest.objects.filter(
        item__in=my_items
    ).exclude(
        status=Status.REJECTED
    ).order_by('-created_at')

    grouped = defaultdict(list)
    for req in donation_requests:
        date = localtime(req.created_at)
        month = date.strftime('%m').lstrip('0')  # '07' → '7'
        day = date.strftime('%d').lstrip('0')    # '08' → '8'
        date_str = f"{month}/{day}"              # '7/8'
        grouped[date_str].append(req)

    print("donation_requests 개수:", donation_requests.count())
    print("grouped keys:", grouped.keys())

    for date, reqs in grouped.items():
        print("날짜:", date)
        for r in reqs:
            print("닉네임:", r.member.nickname, "| 제목:", r.item.title, "| 메모:", r.memo)

    return render(request, 'requests/received_donation_list.html', {
        'grouped': dict(grouped)
    })

# 나눔-보낸 신청 목록 조회 
@login_required
def sent_donation_requests(request):
    member = request.user
    requests = DonationRequest.objects.filter(member=member).order_by('-created_at')

    grouped_requests = defaultdict(list)
    for req in requests:
        date = localtime(req.created_at)
        month = date.strftime('%m').lstrip('0')
        day = date.strftime('%d').lstrip('0')
        date_str = f"{month}/{day}"  # 예: 7/8
        grouped_requests[date_str].append(req)

    return render(request, 'requests/sent_donation_list.html', {
        'grouped_requests': grouped_requests.items()
    })

# 나눔-받은신청(거절처리)
@login_required
def reject_donation_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, pk=request_id)

    if donation_request.item.member != request.user: #그 신청이 내 아이템에 대한 것인지 확인
        messages.error(request, "해당 신청을 거절할 권한이 없습니다.")
        return redirect('received_donation_requests') #권한 없으면 리다이렉트

    donation_request.status = Status.REJECTED
    donation_request.save()

    return redirect('requests:received_donation_requests')

# 나눔-보낸신청(삭제 or 취소 처리)
@login_required
def manage_sent_donation_request(request, request_id, action):
    donation_request = get_object_or_404(DonationRequest, pk=request_id)

    if donation_request.member != request.user:
        messages.error(request, "해당 요청을 처리할 권한이 없습니다.")
        return redirect('requests:sent_donation_requests')

    # 취소(cancel)와 삭제(delete) 모두 삭제로 처리
    if action in ["cancel", "delete"]:
        # WAITING, REJECTED, COMPLETED 상태일 때만 삭제 가능
        if donation_request.status in [Status.WAITING, Status.REJECTED, Status.COMPLETED]:
            donation_request.delete()
            messages.success(request, "신청이 삭제되었습니다.")
        else:
            messages.error(request, "삭제할 수 없는 상태입니다.")
    else:
        messages.error(request, "잘못된 요청입니다.")

    return redirect('requests:sent_donation_requests')


# 교환 - 받은 신청 목록 조회
@login_required
def received_exchange_requests(request):
    print("로그인 상태:", request.user.is_authenticated)
    print("현재 사용자:", request.user.username)

    member = request.user
    my_items = Item.objects.filter(member=member)

    # 거절된 요청 제외
    exchange_requests = ExchangeRequest.objects.filter(
        item__in=my_items
    ).exclude(
        status=Status.REJECTED
    ).order_by('-created_at')

    grouped = defaultdict(list)
    for req in exchange_requests:
        date = localtime(req.created_at)
        month = date.strftime('%m').lstrip('0')  # '07' → '7'
        day = date.strftime('%d').lstrip('0')    # '08' → '8'
        date_str = f"{month}/{day}"              # '7/8'
        grouped[date_str].append(req)

    print("exchange_requests 개수:", exchange_requests.count())
    print("grouped keys:", grouped.keys())

    for date, reqs in grouped.items():
        print("날짜:", date)
        for r in reqs:
            print("닉네임:", r.member.nickname, "| 제목:", r.item.title, "| 메모:", r.memo)

    return render(request, 'requests/received_exchange_list.html', {
        'grouped': dict(grouped)
    })


# 교환-보낸 신청 목록 조회
@login_required
def sent_exchange_requests(request):
    member = request.user
    exchange_requests = ExchangeRequest.objects.filter(member=member).order_by('-created_at')

    return render(request, 'requests/sent_exchange_list.html', {
        'exchange_requests': exchange_requests
    })

# 교환-받은신청(거절처리)
@login_required
def reject_exchange_request(request, request_id):
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)

    if exchange_request.item.member != request.user:
        messages.error(request, "해당 신청을 거절할 권한이 없습니다.")
        return redirect('requests:received_exchange_requests')

    exchange_request.status = Status.REJECTED
    exchange_request.save()

    return redirect('requests:received_exchange_requests')

# 교환-보낸신청(취소/삭제)
@login_required
def manage_sent_exchange_request(request, request_id, action):
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)

    if exchange_request.member != request.user:
        messages.error(request, "해당 요청을 처리할 권한이 없습니다.")
        return redirect('requests:sent_exchange_requests')

    # 취소(cancel)와 삭제(delete) 모두 삭제로 처리
    if action in ["cancel", "delete"]:
        # WAITING, REJECTED, COMPLETED 상태일 때만 삭제 가능
        if exchange_request.status in [Status.WAITING, Status.REJECTED, Status.COMPLETED]:
            exchange_request.delete()
            messages.success(request, "신청이 삭제되었습니다.")
        else:
            messages.error(request, "삭제할 수 없는 상태입니다.")
    else:
        messages.error(request, "잘못된 요청입니다.")

    return redirect('requests:sent_exchange_requests')

