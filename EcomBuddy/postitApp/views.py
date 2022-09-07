from django.shortcuts import render, redirect
from .models import UserPost, UserImage
from .forms import PostForm

# Here we begin using class based views:
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView



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
            just_posted = form.save()
            for img in request.FILES.getlist('images'):
                # TODO "File Validator"
                image = UserImage.objects.create(
                    post=just_posted,
                    image=img,
                )

                pass

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


# Class based views:

class indexView(ListView):
    #model = UserPost
    queryset = UserPost.objects.order_by('-publish_date')
    context_object_name = 'user_posts'
    template_name = 'postitApp/index.html'

class newPost(CreateView):
    template_name = 'postitApp/new_post.html'
    # model = UserPost
    form_class = PostForm
    # fields = ['caption']


class deletePost(DeleteView):
    model = UserPost
    success_url = '/'
    template_name = 'postitApp/delete_object.html'

def aboutPage(request):
    return render(request,'postitApp/about.html', context={})
