from django.forms import Form, ModelForm
from django.db import models
from .models import UserPost

class PostForm(ModelForm):

    class Meta:
        model = UserPost
        fields = ['caption', 'image', 'video']

