from django.contrib.auth.models import AbstractUser
from django.db import models

class Member(AbstractUser):
    username = models.CharField(max_length=12, unique=True)
    nickname = models.CharField(max_length=10)
    region_city = models.CharField(max_length=15 )
    region_district = models.CharField(max_length=15)
    #is_verified = models.BooleanField(default=False)
    star = models.FloatField(default=0)
    image_url = models.CharField(max_length=50, null=True, blank=True)