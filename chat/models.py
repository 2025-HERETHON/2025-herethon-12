from django.db import models
from accounts.models import Member
from requests.models import ExchangeRequest, DonationRequest

class Thread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    donation = models.ForeignKey(DonationRequest, on_delete=models.CASCADE)
    exchange = models.ForeignKey(ExchangeRequest, on_delete=models.CASCADE)

    def __str__(self):
        return f"쪽지방 {self.id}"


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=50, null=True, blank=True)

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"{self.member.nickname}의 메시지 ({self.sent_at})"