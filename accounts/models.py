from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class MemberManager(UserManager):
    pass

class Member(AbstractUser):
    #username = models.CharField(max_length=12, unique=True)
    nickname = models.CharField(max_length=10)
    region_city = models.CharField(max_length=15 )
    region_district = models.CharField(max_length=15)
    region_dong = models.CharField(max_length=15)
    #is_verified = models.BooleanField(default=False)
    star = models.FloatField(default=0)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)    #objects = MemberManager()
    #USERNAME_FIELD = 'username'