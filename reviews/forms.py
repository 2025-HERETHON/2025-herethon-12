from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content', 'image']  # image_url은 이미지 업로드라면 FileField로 바꾸는 것도 가능
