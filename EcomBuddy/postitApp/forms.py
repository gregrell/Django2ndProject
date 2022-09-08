from django.forms import Form, ModelForm
from .models import UserPost, UserImage, UserVideo, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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



class VideoForm(ModelForm):
    class Meta:
        model = UserVideo
        fields = ['video']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            "email",
        )
