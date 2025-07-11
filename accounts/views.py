from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import Member
from posts.models import Item,ItemImage
from reviews.models import Review
from django.db.models import Avg

#로그인
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            #유저 존재
            login(request, user)
            return redirect("home") #추후 home 경로 매핑 필요
            #login 필요한 페이지일 때 비로그인 상태이면 로그인 페이지로 리다이렉트 > 로그인 후 전 페이지로 이동
            next_url = request.GET.get("next") or '/'
            return redirect(next_url)
        else:
            messages.error(request, "아이디 또는 비밀번호를 다시 확인해주세요.")
            #id만 다시 채워주기
            return render(request, "accounts/login.html", {
                "username": username,
            })
    return render(request, "accounts/login.html")


#회원가입
def signup_page(request):
    if request.method == "POST":
        action = request.POST.get("action")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_check = request.POST.get("password-check")
        nickname = request.POST.get("nickname")

        User = get_user_model()
        #아이디 중복 확인
        if action == "check_id":
            if User.objects.filter(username=username).exists():
                messages.error(request, "이미 사용하고 있는 아이디입니다.")
            else:
                messages.success(request, "사용하실 수 있는 아이디입니다.")
            #작성해놨던 아이디, 닉네임 다시 채워주기
            return render(request, "accounts/signup.html", {
                "username": username,
                "nickname": nickname,
            })
        #유저 생성
        elif action == "signup":
            if password != password_check:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
                return render(request, "accounts/signup.html", {
                    "username": username,
                    "nickname": nickname,
                })

            if User.objects.filter(username=username).exists():
                messages.error(request, "이미 사용하고 있는 아이디입니다.")
                return render(request, "accounts/signup.html", {
                    "username": username,
                    "nickname": nickname,
                })
            #비밀번호 자동 해싱 처리
            user = User.objects.create_user(
                username=username,
                password=password,
                nickname=nickname
            )

            login(request, user)
            return redirect("location")

    return render(request, "accounts/signup.html")

#동네 설정
@login_required
def my_region(request):
    if request.method == 'POST':
        member = request.user
        member.region_city = request.POST.get('region_city')
        member.region_district = request.POST.get('region_district')
        member.region_dong = request.POST.get('region_dong')
        member.save()
        logout(request) #자동으로 로그인으로 이동
        #return redirect('home')
    return render(request, 'accounts/location.html')

#상대방 프로필
@login_required
def profile_view(request, pk):
    user = get_object_or_404(Member, pk=pk)

    #해당 유저가 작성한 게시글
    posts = Item.objects.filter(member=user).order_by('-created_at')

    #유저가 받은 후기들
    received_reviews = Review.objects.filter(receiver=user).order_by('-created_at')
    received_review_count = received_reviews.count()

    avg_rating = received_reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    filled_count = int(round(avg_rating * 2))
    stars = range(10)

    return render(request, 'home/profile.html', {
        'profile_user': user,
        'posts': posts,
        'received_reviews': received_reviews,
        'received_review_count': received_review_count,
        'avg_rating': avg_rating,
        'filled_count': filled_count,
        'stars': stars,
    })

#로그아웃
@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('/?success=1')
    return redirect('home')
