from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from posts.models import Item

#카테고리 선택시 화면 랜더링
@login_required
def home_view(request):
    category = request.GET.get('category', '전체')  # None일 때도 '전체'로 처리
    #디폴트 화면
    if category == '전체':
        items = Item.objects.all().order_by('-created_at')[:10]  #최신순 10개 limit, 추후 수정 필요
    else:
        items = Item.objects.filter(category=category).order_by('-created_at') #최신순 정렬

    return render(request, 'home/home_search.html', {
        'items': items,
        'selected_category': category,
    })