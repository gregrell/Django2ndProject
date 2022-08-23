from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    media_path = models.TextField(null=True)
    caption = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(null=True, blank=True)
    alt_caption = models.TextField(max_length=50, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    pass
    def __str__(self): return self.caption
'''
    def delete(self, using=None, keep_parents=False):
        #Override parent
        pass
        stored_image = self.image.storage
        if stored_image.exists(self.image.name):
            stored_image.delete(self.image.name)


        super().delete()

'''

