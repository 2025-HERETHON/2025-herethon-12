from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from accounts.models import Member

#로그인
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            #유저 존재
            login(request, user)
            return redirect("home")
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
                messages.error(request, "중복된 아이디")
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

            return redirect("login")

    return render(request, "accounts/signup.html")

# accounts/views.py
@login_required
def my_page(request):
    return render(request, 'accounts/mypage.html', {'member': request.user})

@login_required
def edit_profile(request):
    member = request.user
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        profile_image = request.FILES.get('profile_image')

        member.nickname = nickname
        if profile_image:
            member.profile_image = profile_image
        member.save()
        return redirect('my_page')

    return render(request, 'accounts/edit_profile.html', {'member': member})

@require_GET
def check_id_duplicate(request):
    username = request.GET.get('username')
    exists = Member.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})
