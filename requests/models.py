from django.db import models
from .enums import Condition, RecommendedAge, Status
from accounts.models import Member
from posts.models import Item

class ExchangeRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    place = models.CharField(max_length=12)
    memo = models.CharField(max_length=200)
    offered_title = models.CharField(max_length=12)
    offered_condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        null=True,
        blank=True
    )
    offered_age = models.CharField(
        max_length=20,
        choices=RecommendedAge.choices,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices,
        default=Status.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="exchange_requests")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="exchange_requests")

    def __str__(self):
        return f"{self.member.nickname}의 교환 신청 ({self.offered_title})"
    
class DonationRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    place = models.CharField(max_length=12)
    memo = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20, 
        choices=Status.choices,
        default=Status.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="donation_requests")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="donation_requests")

    def __str__(self):
        return f"{self.member.nickname}의 나눔 신청"


class ExchangeImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='exchange_images/') #기존 charfiled > imagefiled 변경 / 이미지 자체 저장
    image_order = models.IntegerField()

    request = models.ForeignKey(ExchangeRequest, on_delete=models.CASCADE, related_name="image")

    class Meta:
        ordering = ['image_order']

    def __str__(self):
        return f"{self.request.request_id}번 교환신청 이미지 {self.image_order}"