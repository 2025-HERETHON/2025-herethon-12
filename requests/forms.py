from django import forms
from .models import ExchangeRequest, DonationRequest

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = [
            'place',
            'memo',
            'offered_title',
            'offered_condition',
            'offered_age',
        ]
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 3}),
        }


class DonationRequestForm(forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = [
            'place',
            'memo',
        ]
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 3}),
        }
