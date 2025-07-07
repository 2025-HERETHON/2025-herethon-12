from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from posts.models import Item

#홈 화면 랜더링
@login_required
def home_view(request):
    category = request.GET.get('category', '전체') #카테고리 선택
    keyword = request.GET.get('q', '') #키워드 검색

    #같은 광역시, 시군구 기준 필터링
    user = request.user
    items = Item.objects.filter(
        region_city=user.region_city,
        region_district=user.region_district
    )

    #카테고리
    if category != '전체':
        items = items.filter(category=category)

    #키워드
    if keyword:
        items = items.filter(
            Q(title__icontains=keyword)  #Q(description__icontains=keyword) title에서 검색
        )
        template_name = 'home/home_main.html' #키워드 검색 시 카테고리 ui 사라짐
    else:
        template_name = 'home/home_search.html'

    items = items.order_by('-created_at')[:10] #최신 순 10개 limit, 추후 수정 필요

    return render(request, template_name, {
        'items': items,
        'selected_category': category,
    })
