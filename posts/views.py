from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Item, ItemImage
from .enums import Category, TradeType, Condition, RecommendedAge

#enum 매핑
CATEGORY_MAP = {
    "의류": Category.CLO,
    "수유": Category.FEE,
    "위생": Category.HYG,
    "장난감": Category.TOY,
    "기타": Category.ETC,
}

TRADE_TYPE_MAP = {
    "무료나눔": TradeType.FREE,
    "교환": TradeType.EXCHANGE,
}

CONDITION_MAP = {
    "새상품": Condition.NEW,
    "상태 양호": Condition.LIKE_NEW,
    "사용감 있음(생활 기스/ 오염)": Condition.MINOR,
    "사용감 많음(기능 정상)": Condition.BAD,
}

AGE_MAP = {
    "0~3개월": RecommendedAge.AGE_3,
    "3~6개월": RecommendedAge.AGE_6,
    "6~9개월": RecommendedAge.AGE_9,
    "9~12개월": RecommendedAge.AGE_12,
    "12~18개월": RecommendedAge.AGE_18,
    "18~24개월": RecommendedAge.AGE_24,
    "24~36개월": RecommendedAge.AGE_36,
    "4~5세": RecommendedAge.AGE_5,
    "6~7세": RecommendedAge.AGE_7,
    "8~10세": RecommendedAge.AGE_10,
    "10세 이상": RecommendedAge.AGE_UP,
}

@login_required
def post_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category_text = request.POST.get("category")
        place = request.POST.get("place")
        trade_type_text = request.POST.get("trade_type")
        condition_text = request.POST.get("condition")
        age_text = request.POST.get("age")

        #enum 변환
        category = CATEGORY_MAP.get(category_text)
        trade_type = TRADE_TYPE_MAP.get(trade_type_text)
        condition = CONDITION_MAP.get(condition_text)
        age = AGE_MAP.get(age_text)

        #게시글 저장
        item = Item.objects.create(
            title=title,
            description=description,
            category=category,
            place=place,
            trade_type=trade_type,
            condition=condition,
            age=age,
            region_city=request.user.region_city,
            region_district=request.user.region_district,
            region_dong=request.user.region_dong,
            member=request.user,
        )

        #이미지 저장
        images = request.FILES.getlist("photos")
        for idx, image in enumerate(images):
            ItemImage.objects.create(
                item=item,
                image=image,            
                image_order=idx + 1  #업로드 순서 저장 (수정 로직 추가 필요)
            )

        return redirect("/")

    return render(request, "posts/post.html")
