from django.db import models
from accounts.models import Member
from requests.models import ExchangeRequest, DonationRequest

class Thread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    donation = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, null=True, blank=True)
    exchange = models.ForeignKey(ExchangeRequest, on_delete=models.CASCADE, null=True, blank=True)

    def get_opponent(self, current_user):
        if self.donation:
            return self.donation.member if self.donation.item.member != current_user else self.donation.item.member
        elif self.exchange:
            return self.exchange.member if self.exchange.item.member != current_user else self.exchange.item.member

    def get_item_title(self):
        return self.donation.item.title if self.donation else self.exchange.item.title


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.nickname}의 메시지 ({self.sent_at})"
