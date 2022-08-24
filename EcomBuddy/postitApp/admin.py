from django.contrib import admin
from .models import UserPost, UserImage, UserVideo
# Register your models here.

admin.site.register(UserPost)
admin.site.register(UserImage)
admin.site.register(UserVideo)

