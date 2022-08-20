from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import UserPost
from .forms import PostForm
# Create your views here.


def index(request):
    user_posts = UserPost.objects.all().order_by('-publish_date')
    context = {'user_posts': user_posts}
    return render(request, 'postitApp/index.html', context)

def new_post(request):
    form = PostForm
    context = {'form': form}
    return render(request, 'postitApp/new_post.html', context)

def new_post_submit(request):
    if request.method == "POST":
        user_post = UserPost.objects.create(
            user=request.user,
            caption=request.POST.get('caption')
        )

    return redirect('index')