from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Review
from .forms import ReviewForm
from django.db.models import Avg
from django.utils.timezone import localtime, now
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

# --- 받은/작성한 후기 목록, 평균 별점 ---
@login_required
def my_reviews_view(request):
    user = request.user

    # 내가 작성한 후기
    written_reviews = Review.objects.filter(writer=user).order_by('-created_at')

    # 내가 받은 후기
    received_reviews = Review.objects.filter(receiver=user).order_by('-created_at')

    # 받은 별점 평균
    avg_rating = received_reviews.aggregate(avg=Avg('rating'))['avg']

    # 작성일 -> "~일 전" 변환 함수
    def days_ago_display(date):
        delta = now().date() - date.date()
        if delta.days == 0:
            return "오늘"
        elif delta.days == 1:
            return "어제"
        else:
            return f"{delta.days}일 전"

    written_reviews_formatted = [{
        "review": review,
        "days_ago": days_ago_display(localtime(review.created_at))
    } for review in written_reviews]

    received_reviews_formatted = [{
        "review": review,
        "days_ago": days_ago_display(localtime(review.created_at))
    } for review in received_reviews]

    return render(request, 'reviews/my_reviews.html', {
        'written_reviews': written_reviews_formatted,
        'received_reviews': received_reviews_formatted,
        'avg_rating': round(avg_rating or 0, 1)
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # 작성자 본인만 삭제 가능
    if review.writer != request.user:
        return HttpResponseForbidden("리뷰를 삭제할 권한이 없습니다.")

    review.delete()
    messages.success(request, "리뷰가 삭제되었습니다.")
    return redirect('my_written_reviews')  # 혹은 적절한 리뷰 목록 url name으로 변경