from django.contrib import admin
from .models import UserPost, UserImage, UserVideo, CustomUser, UserFollowing, dog, userDogPreference

# Register your models here.

admin.site.register(UserPost)
admin.site.register(UserImage)
admin.site.register(UserVideo)
admin.site.register(CustomUser)
admin.site.register(UserFollowing)
admin.site.register(dog)
admin.site.register(userDogPreference)
