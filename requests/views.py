from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from requests.models import DonationRequest, ExchangeRequest
from posts.models import Item
from requests.enums import Status
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from reviews.models import Review


# ------------------------
# 기존 신청 관련 뷰들
# ------------------------

# 나눔-받은 신청 목록 조회
@login_required
def received_donation_requests(request):
    member = request.user # 현재 로그인한 유저 
    my_items = Item.objects.filter(member=member) # 내가 올린 용품
    donation_requests = DonationRequest.objects.filter(item__in=my_items).order_by('-created_at') # 최신순 정렬

    return render(request, 'requests/received_donation_list.html', {
        'donation_requests': donation_requests
    })


# 나눔-보낸 신청 목록 조회 
@login_required
def sent_donation_requests(request):
    member = request.user
    donation_requests = DonationRequest.objects.filter(member=member).order_by('-created_at')

    return render(request, 'requests/sent_donation_list.html', {
        'donation_requests': donation_requests
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

    return redirect('received_donation_requests')

# 나눔-보낸신청(삭제 or 취소 처리)
@login_required
def manage_sent_donation_request(request, request_id, action):
    donation_request = get_object_or_404(DonationRequest, pk=request_id)

    if donation_request.member != request.user:
        messages.error(request, "해당 요청을 처리할 권한이 없습니다.")
        return redirect('sent_donation_requests')

    # 상태에 따라 처리
    if action == "cancel":
        if donation_request.status == Status.WAITING:
            donation_request.status = Status.REJECTED  # 취소도 거절로 처리
            donation_request.save()
            messages.success(request, "신청이 취소되었습니다.")
        else:
            messages.error(request, "취소할 수 없는 상태입니다.")

    elif action == "delete":
        if donation_request.status in [Status.REJECTED, Status.COMPLETED]:
            donation_request.delete()
            messages.success(request, "신청이 삭제되었습니다.")
        else:
            messages.error(request, "삭제할 수 없는 상태입니다.")

    return redirect('sent_donation_requests')



# 교환-받은 신청 목록 조회
@login_required
def received_exchange_requests(request):
    member = request.user
    my_items = Item.objects.filter(member=member)
    exchange_requests = ExchangeRequest.objects.filter(item__in=my_items).order_by('-created_at')

    return render(request, 'requests/received_exchange_list.html', {
        'exchange_requests': exchange_requests
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
        return redirect('received_exchange_requests')

    exchange_request.status = Status.REJECTED
    exchange_request.save()

    return redirect('received_exchange_requests')

# 교환-보낸신청(취소/삭제)
@login_required
def manage_sent_exchange_request(request, request_id, action):
    exchange_request = get_object_or_404(ExchangeRequest, pk=request_id)

    if exchange_request.member != request.user:
        messages.error(request, "해당 요청을 처리할 권한이 없습니다.")
        return redirect('sent_exchange_requests')

    if action == "cancel":
        if exchange_request.status == Status.WAITING:
            exchange_request.status = Status.REJECTED
            exchange_request.save()
            messages.success(request, "신청이 취소되었습니다.")
        else:
            messages.error(request, "취소할 수 없는 상태입니다.")

    elif action == "delete":
        if exchange_request.status in [Status.REJECTED, Status.COMPLETED]:
            exchange_request.delete()
            messages.success(request, "신청이 삭제되었습니다.")
        else:
            messages.error(request, "삭제할 수 없는 상태입니다.")

    return redirect('sent_exchange_requests')

# ------------------------
# 마이페이지 - 교환/나눔 내역 조회 뷰
# ------------------------

@login_required
def my_exchange_history(request):
    member = request.user

    # 받은 교환: 내가 올린 글에 대해 누군가 신청한 교환 성사된 것
    received = ExchangeRequest.objects.filter(
        item__member=member,
        status=Status.COMPLETED 
    ).select_related('item', 'member')

    # 보낸 교환: 내가 신청해서 성사된 교환
    sent = ExchangeRequest.objects.filter(
        member=member,
        status=Status.COMPLETED
    ).select_related('item', 'item__member')

    # 리뷰 작성 여부 설정
    for req in list(received) + list(sent):
        req.review_written = Review.objects.filter(exchange_request=req, writer=member).exists()

    # 날짜별 그룹핑
    all_requests = list(received) + list(sent)
    all_requests.sort(key=lambda r: r.updated_at, reverse=True)

    grouped = defaultdict(list)
    for req in all_requests:
        date = localtime(req.updated_at).strftime("%Y.%m.%d")
        grouped[date].append(req)

    return render(request, 'requests/my_exchange_history.html', {
        'grouped': grouped
    })

@login_required
def my_sent_donations(request):
    member = request.user

    completed_requests = DonationRequest.objects.filter(
        item__member=member,
        status=Status.COMPLETED
    ).select_related('item', 'member')

    grouped = defaultdict(list)
    for req in completed_requests:
        date = localtime(req.updated_at).strftime("%Y.%m.%d")
        grouped[date].append(req)

    return render(request, 'requests/my_sent_donations.html', {
        'grouped': grouped
    })


@login_required
def my_received_donations(request):
    member = request.user

    completed_requests = DonationRequest.objects.filter(
        member=member,
        status=Status.COMPLETED
    ).select_related('item', 'item__member')

    for req in completed_requests:
        req.review_written = Review.objects.filter(donation_request=req, writer=member).exists()

    grouped = defaultdict(list)
    for req in completed_requests:
        date = localtime(req.updated_at).strftime("%Y.%m.%d")
        grouped[date].append(req)

    return render(request, 'requests/my_received_donations.html', {
        'grouped': grouped
    })
