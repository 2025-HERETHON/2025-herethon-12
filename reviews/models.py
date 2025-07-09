from django.db import models
from accounts.models import Member
from posts.models import Item

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)

    # 평점: 0.5 ~ 5.0 (0.5 단위)
    rating = models.FloatField()

    # 텍스트 리뷰: 최대 200자
    content = models.CharField(max_length=200)

    # 이미지 1장까지 첨부 가능
    image = models.ImageField(upload_to='review_images/', null=True, blank=True) 

    # 작성일
    created_at = models.DateTimeField(auto_now_add=True)

    # 작성자, 받은 사람
    writer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='written_reviews')
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='received_reviews')

    # 거래 기록 연결: 교환 또는 나눔 중 하나만 연결됨
    exchange_request = models.ForeignKey(
        'user_requests.ExchangeRequest', on_delete=models.SET_NULL, null=True, blank=True
    )
    donation_request = models.ForeignKey(
        'user_requests.DonationRequest', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.writer.nickname} -> {self.receiver.nickname} ({self.rating}점)"
