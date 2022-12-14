from django.forms import Form, ModelForm
from .models import UserPost, UserImage, UserVideo, CustomUser, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class PostForm(ModelForm):
    images = forms.FileField(label='Images',
                             required=False,
                             error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput(attrs={'multiple': True, 'accept': 'image/*'})
                             )

    class Meta:
        model = UserPost
        fields = ['caption', 'images', 'user']
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
        fields = ("email", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'bio']


class YourModelForm(forms.Form):
    comment = forms.CharField(label='the comment', max_length=10)
