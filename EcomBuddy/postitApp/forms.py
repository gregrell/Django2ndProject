from django.forms import Form, ModelForm
from .models import UserPost

class PostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = ['caption', 'image']

