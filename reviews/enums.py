from django.db.models import TextChoices

#왼 > db에 저장되는 값, 오 > 사용자에게 보여 줄 값
#제안 제품 상태
class Condition(TextChoices):
    NEW = 'NEW', '새상품'
    LIKE_NEW = 'LIKE_NEW', '상태 양호'
    MINOR = 'MINOR', '사용감 있음(생활 기스/ 오염)'
    BAD = 'BAD', '사용감 많음(기능 정상)'

#제안 제품 추천 월령
class RecommendedAge(TextChoices):
    AGE_3 = '0_3', '0~3개월'
    AGE_6 = '3_6', '3~6개월'
    AGE_9 = '6_9', '6~9개월'
    AGE_12 = '9_12', '9~12개월'
    AGE_18 = '12_18', '12~18개월'
    AGE_24 = '18_24', '18~24개월'
    AGE_36 = '24_36', '24~36개월'
    AGE_5 = '4_5', '4~5세'
    AGE_7 = '6_7', '6~7세'
    AGE_10 = '8_10', '8~10세'
    AGE_UP = '10+', '10세 이상'

#신청 상태
class Status(TextChoices):
    WAITING = 'WAITING', '대기'
    REJECTED = 'REJECTED', '거절'
    IN_PROGRESS = 'IN_PROGRESS', '거래중'
    COMPLETED = 'COMPLETED', '거래완료'
    