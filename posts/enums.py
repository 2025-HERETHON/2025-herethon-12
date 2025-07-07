from django.db.models import TextChoices

#왼 > db에 저장되는 값, 오 > 사용자에게 보여 줄 값
#카테고리
class Category(TextChoices):
    CLO = '의류', '의류'
    FEE = '수유', '수유'
    HYG = '위생', '위생'
    TOY = '장난감', '장난감'
    ETC = '기타', '기타'
#거래 방식
class TradeType(TextChoices):
    FREE =  '무료 나눔', '무료 나눔'
    EXCHANGE = '교환', '교환'
#제품 상태
class Condition(TextChoices):
    NEW = 'NEW', '새상품'
    LIKE_NEW = 'LIKE_NEW', '상태 양호'
    MINOR = 'MINOR', '사용감 있음(생활 기스/ 오염)'
    BAD = 'BAD', '사용감 많음(기능 정상)'
#추천 월령
class RecommendedAge(TextChoices):
    AGE_3 = '0_3', '0~3개월 추천'
    AGE_6 = '3_6', '3~6개월 추천'
    AGE_9 = '6_9', '6~9개월 추천'
    AGE_12 = '9_12', '9~12개월 추천'
    AGE_18 = '12_18', '12~18개월 추천'
    AGE_24 = '18_24', '18~24개월 추천'
    AGE_36 = '24_36', '24~36개월 추천'
    AGE_5 = '4_5', '4~5세 추천'
    AGE_7 = '6_7', '6~7세 추천'
    AGE_10 = '8_10', '8~10세 추천'
    AGE_UP = '10+', '10세 이상 추천'