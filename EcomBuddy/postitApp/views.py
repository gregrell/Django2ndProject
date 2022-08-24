from django.shortcuts import render, redirect
from django.forms import formset_factory

from .models import UserPost
from .forms import PostForm, ImageForm


# Create your views here.


def index(request):
    user_posts = UserPost.objects.all().order_by('-publish_date')
    context = {'user_posts': user_posts}
    return render(request, 'postitApp/index.html', context)


def new_post(request):
    form = PostForm
    imageform = ImageForm
    context = {'form': form, 'imageform': imageform}
    return render(request, 'postitApp/new_post.html', context)


def new_post_submit(request):
    if request.method == "POST":
        user = request.user
        caption = request.POST.get('caption')
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            for img in request.FILES.getlist('images'):
                # TODO "File Validator"
                pass
            form.save()

        else:
            print('no save')

    return redirect('index')


def delete_post(request, pk):
    try:
        record = UserPost.objects.get(id=pk)
        # record.image.delete() # This deletes the actual file stored at the path of record.image
        # record.video.delete() # This deletes the actual file stored at the path of record.video
        record.delete()
    except:
        print('record does not exist')

    return redirect('index')

