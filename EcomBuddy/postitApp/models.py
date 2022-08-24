from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    caption = models.CharField(max_length=200)
    alt_caption = models.TextField(max_length=50, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.caption


class UserImage(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)


class UserVideo(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    video = models.FileField(null=True, blank=True)
