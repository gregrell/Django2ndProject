from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserPost, UserImage, CustomUser, UserFollowing
from .forms import PostForm, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required

# Here we begin using class based views:
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from django.template.defaulttags import register


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

class indexView(LoginRequiredMixin, ListView):
    # model = UserPost
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    queryset = UserPost.objects.order_by('-publish_date')
    context_object_name = 'user_posts'
    template_name = 'postitApp/index.html'
    def get_queryset(self):
        """return the last fifty posts of the users that the request user follows
        and return to the context object name"""
        user = self.request.user
        following = user.following.filter(user=user)
        """Build list of users for query filter"""
        users = []
        for u in following:
            users.append(u.following)
        """Create query object and build it at runtime"""
        query = Q()
        for name in users:
            query = query | Q(user=name)
        """Chain and filter results"""
        return UserPost.objects.filter(query).order_by('-publish_date')[:50]

    def get_context_data(self, **kwargs):
        """ need to have multiple queries beyond the get_queryset call. Construct a dictionary and call
        the super class get_context_data to get the 'user_posts' context as queried above in get_queryset
        this is returned as a dict. Then add additional items as needed to the dict before returning it"""
        cd = super(indexView, self).get_context_data(**kwargs)
        cd['not_following'] = CustomUser.objects.all()
        u_list = cd.get('not_following')
        fq = {}  # following query dictionary creation
        """ Create the following query dictionary for all the suggested users """
        for u in u_list:
            following_query = UserFollowing.objects.filter(following=u)
            fq[u.username] = following_query
        cd['fq'] = fq  # add the feature query dictionary to the context data dictionary
        return cd

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class newPost(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'postitApp/new_post.html'
    # model = UserPost
    form_class = PostForm
    # fields = ['caption']


class deletePost(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
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


@login_required()
def editUser(request):
    user = request.user
    form = CustomUserChangeForm(instance=user)

    following = user.following.filter(user=user)
    followed_by = user.followed_by.filter(following=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('edit-user')

    else:
        return render(request, 'postitApp/registration/settings.html', context={'form': form,
                                                                                'following': following,
                                                                                'followed_by': followed_by})


@login_required()
def logoutUser(request):
    logout(request)
    return redirect('index')

def publicProfile(request,pk):
    context = {}
    return render(request, 'postitApp/profile/public_profile.html', context)
