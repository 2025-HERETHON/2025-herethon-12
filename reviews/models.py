from django.db import models
from accounts.models import Member
#from .models import Donation, Exchange

# Create your models here.
#class Review(models.Model):
    #review_id = models.AutoField(primary_key=True)
    #rating = models.FloatField()
    #content = models.CharField(max_length=200)
    #image_url = models.CharField(max_length=50, null=True, blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    #writer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='writex_review')
    #receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='receive_review')
    #donation = models.ForeignKey('item.Donation', on_delete=models.SET_NULL, null=True, blank=True)
    #exchange = models.ForeignKey('item.Exchange', on_delete=models.SET_NULL, null=True, blank=True)
