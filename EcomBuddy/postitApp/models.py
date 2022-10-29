from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


# Define function to save to the user folder. Taken from Django user documentation
def user_directory_path(instance, filename):
    try:
        # Saving profile picture from user settings
        id = instance.id
    except:
        # Saving media from creating a new post
        id = instance.post.created_by.id
    return 'user_{0}/{1}'.format(id, filename)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to=user_directory_path, null=True, default="avatar.svg")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # username (super)
    # firstname (super)
    # lastname (super)


    def __str__(self):
        return self.username


class UserPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts', null=True) # CustomUser.posts.all()
    caption = models.CharField(max_length=200)
    alt_caption = models.TextField(max_length=50, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.caption  # Keep in mind, this will return as primary key


class UserImage(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)


class UserVideo(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    video = models.FileField(null=True, blank=True)

class UserFollowing(models.Model):
    user = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE, null=True, blank=False)
    following = models.ForeignKey(CustomUser,
                                  related_name='followed_by',
                                  on_delete=models.CASCADE,
                                  null=True,
                                  blank=False)
    #TODO date field for when followed occured

    class Meta:
        unique_together = ['user', 'following']


class LikesTable(models.Model):
    #TODO implement
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, null=False, blank=False)
    liked_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ['user', 'post']
