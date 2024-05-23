from django.db import models

# Create your models here.

# models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 追加したいフィールドを定義する
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)