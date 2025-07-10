from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Review
from .forms import ReviewForm
from django.db.models import Avg
from django.utils.timezone import localtime, now
from requests.models import ExchangeRequest, DonationRequest
from collections import defaultdict
from reviews.models import Review
from requests.enums import Status
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from accounts.models import Member
from django.contrib.auth import get_user_model

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

                #별점 평균 receiver에 반영 > 반올림
                avg_rating = Review.objects.filter(receiver=receiver).aggregate(avg=Avg('rating'))['avg'] or 0
                receiver.star = round(avg_rating, 1)
                receiver.save()

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



# --- 마이페이지, 프로필 수정 ---

@login_required
def my_page(request):
    return render(request, 'reviews/mypage.html', {'member': request.user})

@login_required
def edit_profile(request):
    member = request.user
    if request.method == 'POST':
        action = request.POST.get("action")
        username = request.POST.get("username")
        nickname = request.POST.get('nickname')
        profile_image = request.FILES.get('profile_image')
        User = get_user_model()

        # 아이디 중복확인 (signup에서 가져옴)
        if action == "check_id":
            if User.objects.filter(username=username).exists():
                messages.error(request, "이미 사용하고 있는 아이디입니다.")
            else:
                messages.success(request, "사용하실 수 있는 아이디입니다.")
            #작성해놨던 아이디, 닉네임 다시 채워주기
            return render(request, "reviews/edit.html", {
                "username": username,
                "nickname": nickname,
                "profile_image": profile_image,
                "member": member, 
            })

        member.username = username
        member.nickname = nickname
        if profile_image:
            member.image = profile_image
        member.save()
        return redirect('my_page')

    return render(request, 'reviews/edit.html', {'member': member})

# ------------------------
# 마이페이지 - 교환/나눔 내역 조회 뷰
# ------------------------

@login_required
def my_exchange_history(request):
    member = request.user

    # 받은 교환: 내가 올린 글에 누군가 신청해서 성사된 것
    received = ExchangeRequest.objects.filter(
        item__member=member,
        status=Status.COMPLETED
    ).select_related('item', 'member')

    # 보낸 교환: 내가 신청해서 성사된 것
    sent = ExchangeRequest.objects.filter(
        member=member,
        status=Status.COMPLETED
    ).select_related('item', 'item__member')

    # 리뷰 작성 여부 추가
    for req in list(received) + list(sent):
        req.review_written = Review.objects.filter(exchange_request=req, writer=member).exists()

    # 날짜별 그룹핑
    all_requests = list(received) + list(sent)
    all_requests.sort(key=lambda r: r.updated_at, reverse=True)

    grouped = defaultdict(list)
    for req in all_requests:
        date = localtime(req.updated_at).date()
        month = date.strftime('%m').lstrip('0')
        day = date.strftime('%d').lstrip('0')
        date_str = f"{month}/{day}"
        grouped[date_str].append(req)

    # 날짜 내림차순 정렬 (최신 날짜 위로)
    grouped = dict(sorted(grouped.items(), reverse=True))

    return render(request, 'reviews/change.html', {
        'grouped': dict(grouped),
        'user': request.user
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
        date = localtime(req.created_at).date()
        month = date.strftime('%m').lstrip('0')  # '07' → '7'
        day = date.strftime('%d').lstrip('0')    # '08' → '8'
        date_str = f"{month}/{day}"              # '7/8'
        grouped[date].append(req)

    # 날짜 내림차순 정렬 (최신 날짜 위로)
    grouped = dict(sorted(grouped.items(), reverse=True))

    return render(request, 'reviews/sent-share.html', {
        'grouped': grouped
    })


@login_required
def my_received_donations(request):
    print("🔥 my_received_donations 뷰 함수 호출됨")
    member = request.user
    print("현재 로그인한 사용자:", member)

    completed_requests = DonationRequest.objects.filter(
        member=member,
        status=Status.COMPLETED
    ).select_related('item', 'item__member')
    print("완료된 받은 나눔 개수:", completed_requests.count())

    for req in completed_requests:
        req.review_written = Review.objects.filter(donation_request=req, writer=member).exists()
        print("리뷰 작성 여부:", req.review_written)
        print("아이템 제목:", req.item.title)
        print("아이템 작성자 닉네임:", req.item.member.nickname)
        print("아이템 설명:", req.item.description)
        
        print("업데이트 일자:", req.updated_at)

    grouped = defaultdict(list)
    for req in completed_requests:
        date = localtime(req.created_at).date()
        month = date.strftime('%m').lstrip('0')  # '07' → '7'
        day = date.strftime('%d').lstrip('0')    # '08' → '8'
        date_str = f"{month}/{day}"              # '7/8'
        grouped[date].append(req)

    # 날짜 내림차순 정렬 (최신 날짜 위로)
    grouped = dict(sorted(grouped.items(), reverse=True))
    
    print("✅ 최종 grouped 전달 데이터:")
    for k, v in grouped.items():
        print(f"날짜: {k}, 개수: {len(v)}")

    return render(request, 'reviews/share.html', {
        'grouped': dict(grouped)
    })

@require_GET
def check_id_duplicate(request):
    username = request.GET.get('username')
    exists = Member.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

def change_view(request):
    return render(request, 'reviews/change.html')

def share_view(request):
    return render(request, 'reviews/share.html')

def myreview_view(request):
    return render(request, 'reviews/myreview.html')

def mypage_view(request):
    return render(request, 'reviews/mypage.html')