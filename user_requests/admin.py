from django.contrib import admin
from .models import ExchangeRequest, DonationRequest, ExchangeImage

# Register your models here.
admin.site.register(ExchangeRequest)
admin.site.register(DonationRequest)
admin.site.register(ExchangeImage)