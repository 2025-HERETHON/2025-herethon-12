from django.shortcuts import render
from posts.models import Item

# Create your views here.
def home_view(request):
    items = Item.objects.all().order_by("-created_at")[:10]
    return render(request, "home/home_main.html", {"items": items})