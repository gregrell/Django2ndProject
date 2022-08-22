from django.shortcuts import render, redirect

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
        user = request.user
        caption = request.POST.get('caption')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('save')

        else:
            print('no save')

    return redirect('index')


def delete_post(request, pk):
    try:
        record = UserPost.objects.get(id=pk)
        record.delete()
    except:
        print('record does not exist')

    return redirect('index')

