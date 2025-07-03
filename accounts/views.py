from django.shortcuts import render
from django.http import JsonResponse
from .models import Member

# Create your views here.
#회원가입 랜더링
def signup_page(request):
    return render(request, 'accounts/signup.html')

#회원가입 - 아이디 중복 확인
def check_id_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if Member.objects.filter(username=username).exists():
            print("중복된 아이디")
        else:
            print("사용 가능한 아이디")
        return render(request, "accounts/signup.html", {"username": username})
    else:
        return render(request, "accounts/signup.html")