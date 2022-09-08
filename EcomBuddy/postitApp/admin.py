from django.contrib import admin
from .models import UserPost, UserImage, UserVideo, CustomUser
# Register your models here.

admin.site.register(UserPost)
admin.site.register(UserImage)
admin.site.register(UserVideo)
admin.site.register(CustomUser)

