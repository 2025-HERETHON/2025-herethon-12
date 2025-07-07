from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from posts.models import Item

# Create your views here.
@login_required
def home_view(request):
    category = request.GET.get('category', None)

    #디폴트 화면
    if category is None:
        items = Item.objects.all().order_by('-created_at')[:10] #최신순 10개 limit, 추후 수정 필요
        return render(request, 'home/home_search.html', {
            'items': items,
            'selected_category': '전체',
        })
    else: #카테고리 선택 시
        if category == '전체':
            items = Item.objects.all().order_by('-created_at')
        else:
            items = Item.objects.filter(category=category).order_by('-created_at')

        return render(request, 'home/home_main.html', {
            'items': items,
            'selected_category': category,
        })
