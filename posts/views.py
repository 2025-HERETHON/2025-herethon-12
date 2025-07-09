from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, ItemImage
from user_requests.models import DonationRequest, ExchangeRequest, ExchangeImage
from .enums import Category, TradeType, Condition, RecommendedAge
from django.db.models import Max

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
@login_required
def post_update(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    if request.user != item.member:
        return HttpResponse("<script>history.back();</script>") #작성자가 아니면 수정 권한 X

    if request.method == 'POST':
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

        # 게시글 수정
        item.title = title
        item.description = description
        item.category = category
        item.place = place
        item.trade_type = trade_type
        item.condition = condition
        item.age = age
        item.save()

        # 기존 이미지에 추가하기 위한 정보 확인
        last_order = (
            ItemImage.objects.filter(item=item).aggregate(Max("image_order"))["image_order__max"] or 0
        )

        #이미지 저장
        images = request.FILES.getlist("photos")
        for idx, image in enumerate(images):
            ItemImage.objects.create(
                item=item,
                image=image,            
                image_order= last_order + idx + 1  #업로드 순서 저장 (수정 로직 추가 필요)
            )

        return redirect('post_detail', item_id=item.item_id)
    
    # 기존 이미지 조회
    item_images = ItemImage.objects.filter(item=item).order_by("image_order")
    image_urls = [img.image.url for img in item_images]
    existing_images = [""] + image_urls # 인덱스 012 말고 123으로 image_order랑 맞추기

    return render(request, "posts/update.html", {
            "item": item,
            "existing_images": existing_images
        })

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

    # 신청
    if request.method == "POST":
        # 신청한 적 있냐
        if ExchangeRequest.objects.filter(item=item, member=request.user).exists():
            return HttpResponse("<script>history.back();</script>")

        place = request.POST.get("place")
        title = request.POST.get("title")
        memo = request.POST.get("description")
        condition_text = request.POST.get("condition")
        age_text = request.POST.get("age")

        # enum 변환
        condition = CONDITION_MAP.get(condition_text)
        age = AGE_MAP.get(age_text)

        exchange_request_obj = ExchangeRequest.objects.create(
            place=place,
            memo=memo,
            offered_title=title,
            offered_condition=condition,
            offered_age=age,
            item=item,
            member=request.user,
        )

        # 이미지 저장
        images = request.FILES.getlist("photos")
        for idx, image_file in enumerate(images):
            ExchangeImage.objects.create(
                request=exchange_request_obj,
                image=image_file,
                image_order=idx + 1
            )

        #return redirect(f"{reverse('exchange_request', args=[item_id])}?success=1")
        return JsonResponse({'redirect_url': reverse('post_detail', args=[item_id])})
    #GET 요청 처리
    show_modal = request.GET.get("success") == "1"
    return render(request, 'posts/exchange.html', {
        'item': item,
        'show_modal': show_modal,
    })


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