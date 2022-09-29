from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserPost, UserImage, CustomUser
from .forms import PostForm, CustomUserCreationForm, CustomUserChangeForm

# Here we begin using class based views:
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login, logout, authenticate


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        user_posts = UserPost.objects.all().order_by('-publish_date')
        context = {'user_posts': user_posts}
        return render(request, 'postitApp/index.html', context)

    else:
        return render(request, 'postitApp/registration/landing_page.html', context={})


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
            form.instance.created_by = request.user
            just_posted = form.save(commit=True)

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
    # model = UserPost
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
    return render(request, 'postitApp/about.html', context={})


def landingPage(request):
    return render(request, 'postitApp/registration/landing_page.html', context={})


def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = CustomUser.objects.get(email=email.lower()).username
            user = authenticate(username=username, password=password)
        except:
            user = None
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "User or Password not found")

    return render(request, 'postitApp/registration/login.html', context={})


def signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = form.save(commit=False)
            user.username = email.lower()
            try:
                user.save()
                login(request, user)
                return redirect('index')
            except:
                messages.error(request, "Could not save user")

    else:
        messages.error(request, "Could not register user")

    return render(request, 'postitApp/registration/signup.html', context={'form': form})

def editUser(request):
    pass



def logoutUser(request):
    logout(request)
    return redirect('index')
