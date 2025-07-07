from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from posts.models import Item

# Create your views here.
@login_required
def home_view(request):
    items = Item.objects.all().order_by("-created_at")[:10] #최신순 10개 > 추후 수정 필요
    return render(request, "home/home_main.html", {"items": items})