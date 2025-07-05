from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Review
from .forms import ReviewForm
from requests.models import ExchangeRequest, DonationRequest

@login_required
def create_review(request, request_type, request_id):
    writer = request.user

    # --- 교환 후기 작성 ---
    if request_type == 'exchange':
        exchange = get_object_or_404(ExchangeRequest, pk=request_id)

        # 쌍방 모두 후기를 남길 수 있도록 조건 분기
        if writer == exchange.member: # 내가 신청한 경우
            receiver = exchange.item.member
        elif writer == exchange.item.member: # 상대방이 신청한 경우 
            receiver = exchange.member
        else:
            return HttpResponseForbidden("후기를 작성할 권한이 없습니다.")

        # 이미 리뷰를 작성한 경우
        if Review.objects.filter(exchange_request=exchange, writer=writer).exists():
            messages.error(request, "이미 후기를 작성하셨습니다.")
            return redirect('my_exchange_history')

        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.writer = writer
                review.receiver = receiver
                review.exchange_request = exchange
                review.save()
                messages.success(request, "후기가 등록되었습니다.")
                return redirect('my_exchange_history')
        else:
            form = ReviewForm()

        return render(request, 'reviews/review_form.html', {
            'form': form,
            'item': exchange.item,
            'receiver': receiver
        })

    # --- 나눔 후기 작성 ---
    elif request_type == 'donation':
        donation = get_object_or_404(DonationRequest, pk=request_id)

        # 받은 사람만 작성 가능
        if writer != donation.member:
            return HttpResponseForbidden("후기를 작성할 권한이 없습니다.")

        receiver = donation.item.member

        if Review.objects.filter(donation_request=donation, writer=writer).exists():
            messages.error(request, "이미 후기를 작성하셨습니다.")
            return redirect('my_donation_history_received')

        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.writer = writer
                review.receiver = receiver
                review.donation_request = donation
                review.save()
                messages.success(request, "후기가 등록되었습니다.")
                return redirect('my_donation_history_received')
        else:
            form = ReviewForm()

        return render(request, 'reviews/review_form.html', {
            'form': form,
            'item': donation.item,
            'receiver': receiver
        })

    # 잘못된 request_type 처리
    else:
        return HttpResponseForbidden("잘못된 요청입니다.")
