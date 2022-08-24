from django.forms import Form, ModelForm
from django.db import models
from .models import UserPost, UserImage, UserVideo
from django import forms


class PostForm(ModelForm):
    images = forms.FileField(label='Images',
                             required=False,
                             error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput(attrs={'multiple': True, 'accept': 'image/*'})
                             )

    class Meta:
        model = UserPost
        fields = ['caption', 'images']
        widgets = {
            "caption": forms.TextInput(attrs={'autocomplete': 'off'})
        }




class ImageForm(ModelForm):
    class Meta:
        model = UserImage
        fields = ['image']


class VideoForm(ModelForm):
    class Meta:
        model = UserVideo
        fields = ['video']

