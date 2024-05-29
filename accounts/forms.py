# forms.py
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'profile_pic', 'bio', 'location')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザーID'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード（確認用）'
        self.fields['bio'].label = '自己紹介'
        self.fields['location'].label = '学部'
        self.fields['profile_pic'].label = 'プロフィール画像'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',  'bio', 'location', 'profile_pic')
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].label = '自己紹介'
        self.fields['location'].label = '場所'
        self.fields['profile_pic'].label = 'プロフィール画像'
        self.fields