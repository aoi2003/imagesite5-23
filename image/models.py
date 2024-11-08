from django.db import models
from django.conf import settings
from .consts import MAX_RATE

CATEGORY = (
    ('kawaii', 'かわいい'),
    ('cool', 'かっこいい'),
    ('other', 'その他')
)

RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)]

class Image(models.Model):
    title = models.CharField('タイトル', max_length=100)
    text = models.TextField('説明')
    thumbnail = models.ImageField('サムネイル画像', null=True, blank=True)
    category = models.CharField('カテゴリ', max_length=100, choices=CATEGORY)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Review for {self.image.title} by {self.user}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    target = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.target}"
