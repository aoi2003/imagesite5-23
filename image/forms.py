from django import forms
from .models import Image,Review

class CreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'text', 'category', 'thumbnail')
        labels = {
            'title': 'タイトル',
            'text': '本文',
            'category': 'カテゴリ',
            'thumbnail': 'サムネイル画像',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'text']