from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, ItemImage
from requests.models import DonationRequest, ExchangeRequest
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
    "무료 나눔": TradeType.FREE,
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

#------------------<<게시글>>---------------------

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

        return redirect("home")

    return render(request, "posts/post.html")

#게시글 상세 조회
@login_required
def post_detail(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    is_writer = request.user == item.member #본인 여부
    already_request = False

    if not is_writer: #작성자 아닐 경우, 이미 신청한 적 있는지 검사
        if(item.trade_type == "무료 나눔"):
            already_request = DonationRequest.objects.filter(item=item, member=request.user).exists()
        else:
            already_request = ExchangeRequest.objects.filter(item=item, member=request.user).exists()

    return render(request, 'posts/detail.html', {
        'item': item,
        'is_writer': is_writer,
        'already_request': already_request
    })

#게시글 수정

#게시글 삭제
@login_required
def post_delete(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    if request.user != item.member:
        return HttpResponse("<script>history.back();</script>") #작성자가 아니면 삭제 권한 X

    if request.method == 'POST':
        item.delete()
        return redirect('home') #삭제 후

    return HttpResponse("<script>history.back();</script>")

#------------------<<교환>>---------------------
#교환 신청
@login_required
def exchange_request(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)

    if request.user == item.member:
        return HttpResponse("<script>history.back();</script>")  # 작성자이면 본인 게시글에 대한 신청 막아둠

    #신청한 적 있냐
    if ExchangeRequest.objects.filter(item=item, member=request.user).exists():  # 신청한 적 있음
        return HttpResponse("<script>history.back();</script>")


    return render(request, 'posts/exchange.html')


#나눔 신청
@login_required
def donation_request(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)

    if request.user == item.member:
        return HttpResponse("<script>history.back();</script>") #작성자이면 본인 게시글에 대한 신청 막아둠

    #신청
    if request.method == "POST":
        #신청한 적 있냐
        if DonationRequest.objects.filter(item=item, member=request.user).exists():
            return HttpResponse("<script>history.back();</script>")

        place = request.POST.get("place")
        memo = request.POST.get("description")

        DonationRequest.objects.create(
            place=place,
            memo=memo,
            item=item,
            member=request.user, #신청자
        )
        return redirect(f"{reverse('donation_request', args=[item_id])}?success=1")

    #모달 띄울 여부 전달
    show_modal = request.GET.get("success") == "1"
    return render(request, 'posts/free.html', {
        'item': item,
        'show_modal': show_modal,
    })