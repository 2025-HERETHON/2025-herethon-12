from django.db import models
from .enums import Category, TradeType, Condition, RecommendedAge
from accounts.models import Member

# Create your models here.
class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=12)
    description = models.CharField(max_length=200)
    category = models.CharField(
        max_length=3,
        choices=Category.choices,
    )
    place = models.CharField(max_length=12)
    trade_type = models.CharField(
        max_length=4,
        choices=TradeType.choices,
    )
    condition = models.CharField(
        max_length=15,
        choices=Condition.choices,
        null=True,
        blank=True
    )
    age = models.CharField(
        max_length=10,
        choices=RecommendedAge.choices,
        null=True,
        blank=True
    )
    sold_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ItemImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=50)
    image_order = models.IntegerField()

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='image')
