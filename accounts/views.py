from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Member

# Create your views here.
#회원가입 랜더링
def signup_page(request):
    if request.method == "POST":
        action = request.POST.get("action")  #check_id or signup
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_check = request.POST.get("password-check")
        nickname = request.POST.get("nickname")

        if action == "check_id": #아이디 중복 확인
            if Member.objects.filter(username=username).exists():
                messages.error(request, "중복된 아이디")
            else:
                messages.success(request, "사용 가능")
            return render(request, "accounts/signup.html", {
                "username": username,
                "nickname": nickname})

        elif action == "signup": #회원가입
            #비밀번호 확인
            if password != password_check:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
                return render(request, "accounts/signup.html", {
                    "username": username,
                    "nickname": nickname,
                })

            #아이디 중복 확인
            if Member.objects.filter(username=username).exists():
                messages.error(request, "중복된 아이디")
                return render(request, "accounts/signup.html", {
                    "username": username,
                    "nickname": nickname,
                })

            Member.objects.create(
                username=username,
                password=make_password(password),
                nickname=nickname
            )
            return redirect("login")

    return render(request, "accounts/signup.html")