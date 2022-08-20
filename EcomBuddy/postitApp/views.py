from django.shortcuts import render
from django.http import HttpResponse
from .models import UserPost
# Create your views here.


def index(request):
    user_posts = UserPost.objects.all().order_by('-publish_date')
    context = {'user_posts': user_posts}
    return render(request, 'postitApp/index.html', context)

def new_post(request):
    context = {}
    return render(request, 'postitApp/new_post.html', context)
