from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    media_path = models.TextField(null=True)
    caption = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    alt_caption = models.TextField(max_length=50, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    pass
    def __str__(self): return self.caption

