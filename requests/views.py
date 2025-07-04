from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from requests.models import DonationRequest
from posts.models import Item
from requests.enums import Status

# 나눔-받은 신청 목록 조회
def received_donation_requests(request):
    member = request.user # 현재 로그인한 유저 
    my_items = Item.objects.filter(member=member) # 내가 올린 용품
    donation_requests = DonationRequest.objects.filter(item__in=my_items).order_by('-created_at') # 최신순 정렬

    return render(request, 'requests/received_donation_list.html', {
        'donation_requests': donation_requests
    })

# 나눔-보낸 신청 목록 조회 
def sent_donation_requests(request):
    member = request.user
    donation_requests = DonationRequest.objects.filter(member=member).order_by('-created_at')

    return render(request, 'requests/sent_donation_list.html', {
        'donation_requests': donation_requests
    })

# 나눔-받은신청(거절처리)
def reject_donation_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, pk=request_id)

    if donation_request.item.member != request.user: #그 신청이 내 아이템에 대한 것인지 확인
        messages.error(request, "해당 신청을 거절할 권한이 없습니다.")
        return redirect('received_donation_requests') #권한 없으면 리다이렉트

    donation_request.status = Status.REJECTED
    donation_request.save()

    return redirect('received_donation_requests')

# 나눔-보낸신청(삭제 or 취소 처리)
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
