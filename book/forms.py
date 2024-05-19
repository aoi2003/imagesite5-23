from django import forms
from .models import Book

class CreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'text', 'category', 'thumbnail')
        labels = {
            'title': 'タイトル',
            'text': '本文',
            'category': 'カテゴリ',
            'thumbnail': 'サムネイル画像',
        }