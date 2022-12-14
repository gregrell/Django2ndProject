import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserPost, UserImage, CustomUser, UserFollowing, LikesTable, dog, userDogPreference
from .forms import PostForm, CustomUserCreationForm, CustomUserChangeForm, YourModelForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# Here we begin using class based views:
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from django.template.defaulttags import register
from django.http import HttpResponse

# HTMX Imports
from django_htmx.http import trigger_client_event


# Create your views here.


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


def queryUserPostFeed(request):
    """return the last fifty posts of the users that the request user follows
          and return to the context object name"""
    user = request.user
    following = user.following.filter(user=user)
    """Build list of users for query filter"""
    users = []
    for u in following:
        users.append(u.following)
    """Create query object and build it at runtime"""

    if len(users) is not 0:
        query = Q()
        for name in users:
            query = query | Q(user=name)
        """Chain and filter results"""
        posts = UserPost.objects.filter(query).order_by('-publish_date')[:50]
    else:
        posts = None
    return posts


@login_required()
def generateNotFollowingPool(request):
    """ Generate a pool of unfollowed users for creating dynamic suggested following list. Store
     on session object """
    number_results = 50
    all_user_id_list = list(CustomUser.objects.all().values_list('id', flat=True))
    followed_user_id_list = list(UserFollowing.objects.filter(user=request.user).values_list('following',
                                                                                             flat=True))
    all_user_not_followed_id_set = set(all_user_id_list) - set(followed_user_id_list)
    all_user_not_followed_id_list = list(all_user_not_followed_id_set)
    sample_size = len(all_user_not_followed_id_list) if len(
        all_user_not_followed_id_list) < number_results else number_results
    suggested_unfollowed_users_list = random.sample(all_user_not_followed_id_list, sample_size)

    request.session['unfollowed_pool'] = suggested_unfollowed_users_list
    return None


@login_required()
def generateNotFollowingList(request, number_results):
    """ Generate a random set of people that are not followed for the suggested users to follow
           do this by getting all users as list, then getting all followed users, convert them to a set
           then do set subtraction operation, convert the result to a list, and use random to pick 5 from that list
           if the set size is less than 10 users, this is handled by sample_size one line conditional"""
    if not number_results:
        number_results = 5

    unfollowed_pool = request.session.get('unfollowed_pool')
    number_results = len(unfollowed_pool) if len(unfollowed_pool) < number_results else number_results
    suggested_unfollowed_users_list, unfollowed_pool_remaining = unfollowed_pool[:number_results], unfollowed_pool[
                                                                                                   number_results:]
    request.session['unfollowed_pool'] = unfollowed_pool_remaining

    context_dict = {'not_following': CustomUser.objects.filter(pk__in=suggested_unfollowed_users_list)}
    u_list = context_dict.get('not_following')
    fq = {}  # following query dictionary creation for showing the number of followers that an unfollowed user has
    """ Create the following query dictionary for all the suggested users """
    for u in u_list:
        following_query = UserFollowing.objects.filter(following=u)
        fq[u.username] = following_query
    context_dict['fq'] = fq  # add the feature query dictionary to the context data dictionary
    return context_dict

@login_required()
def likesQuery(request, post):
    likes_query = LikesTable.objects.filter(post=post)
    return likes_query

@login_required()
def queryIfUserLikedPost(request, posts):
    lq = {}
    request_user_liked_post = {}
    if not posts is None:
        for post in posts:
            likes_query = likesQuery(request, post)
            lq[post] = likes_query
            users_who_liked_post = likes_query.values('user_id')
            for user in users_who_liked_post:
                if request.user.id in user.values():
                    request_user_liked_post[post] = True

    return lq, request_user_liked_post


# Class based views:

class IndexView(LoginRequiredMixin, ListView):
    # model = UserPost
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    queryset = UserPost.objects.order_by('-publish_date')
    context_object_name = 'user_posts'
    template_name = 'postitApp/index.html'

    def get_queryset(self):
        posts = queryUserPostFeed(self.request)
        return posts

    def get_context_data(self, **kwargs):
        """ need to have multiple queries beyond the get_queryset call. Construct a dictionary and call
        the super class get_context_data to get the 'user_posts' context as queried above in get_queryset
        this is returned as a dict. Then add additional items as needed to the dict before returning it"""
        generateNotFollowingPool(self.request)
        cd = super(IndexView, self).get_context_data(**kwargs)
        not_following = generateNotFollowingList(self.request, 5)
        cd['not_following'] = not_following.get('not_following')
        cd['fq'] = not_following.get('fq')  # add the feature query dictionary to the context data dictionary
        """ Get the likes and comments for each post. Place this in context data. """

        if not cd.get('user_posts') is None:
            cd['lq'], cd['request_user_liked_post'] = queryIfUserLikedPost(self.request, cd.get('user_posts'))
        return cd


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class NewPost(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'postitApp/new_post.html'
    # model = UserPost
    form_class = PostForm
    # fields = ['caption']


class DeletePost(LoginRequiredMixin, DeleteView):
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


""" This method called when the logged in user wishes to view their own public profile page """


@login_required()
def publicProfile(request, pk):
    context = {}
    return render(request, 'postitApp/profile/public_profile.html', context)


""" This method called when user selects to unfollow another user pk=user_id to unfollow """


@login_required()
def unfollowUser(request, pk):
    try:
        relationsip = UserFollowing.objects.get(user=request.user, following=pk)
        relationsip.delete()
    except:
        pass
    return redirect('index')


""" This method called when user selects to follow another user's public profile pk=user_id to follow """


@login_required()
def followUser(request, pk):
    requesting_user = CustomUser.objects.get(pk=request.user.id)
    followed_user = CustomUser.objects.get(pk=pk)

    """ SQL Lite does not enforce unique_together uniqueness, therefore have to 
    implement in logic. Try to find the relationhip. If it exists then there's no error, don't save
    if the relationship search does throw an error, then it does not exist. Create the relationship."""

    try:
        UserFollowing.objects.get(user=requesting_user, following=followed_user)
        print('following already exists')
        # TODO generate error message to template
    except:
        relationship = UserFollowing(user=requesting_user, following=followed_user)
        relationship.save()

    return HttpResponse('')


""" This method called if the user performs a like on a post. Check to see if like exists, 
 if not then generate instance and save in database. If the like already exists, then unlike
  by deleting the existing entry """


@login_required()
def likePost(request, post_id):
    post_instance = UserPost.objects.get(id=post_id)
    like = LikesTable(user=request.user, post=post_instance)
    """ see if this instance already exists """
    existing_like = LikesTable.objects.filter(user=request.user, post=post_instance)
    if not existing_like:
        """ Like the post by saving the new instance in the database """
        like.save()
    else:
        """ Unlike the post by deleting the existing database instance """
        existing_like.delete()

    queryset = UserPost.objects.order_by('-publish_date')

    cd = {'lq': (queryIfUserLikedPost(request, queryset))[0],
          'request_user_liked_post': (queryIfUserLikedPost(request, queryset))[1], 'post': post_instance}

    response = render(request, 'postitApp/HTMX/Partials/like_fire_icon.html', cd)
    trigger_client_event(response, 'updated_likes' + str(post_id), {})
    return response


""" HTMX Playground """


@login_required()
def htmxPlay(request):
    form = CustomUserCreationForm()
    emoji_form = YourModelForm()
    posts = request.user.posts.all()
    context = {'form': form, 'posts': posts, 'emoji_form': emoji_form}
    return render(request, 'postitApp/HTMX/htmx_play.html', context)


""" htmx called method to determine if a user email exists """


@login_required()
@require_http_methods(['POST'])
def checkUsername(request):
    email = request.POST.get('email')
    if CustomUser.objects.filter(email=email).exists():
        return HttpResponse("<div style='color:red;'>This email already exists</div>")
    else:
        return HttpResponse("<div style='color:green;'>Available</div>")


""" htmx create a non image user post """


@login_required()
@require_http_methods(['POST'])
def createnoimagepost(request):
    caption = request.POST.get('captiontext')
    post = UserPost.objects.get_or_create(caption=caption)[0]
    request.user.posts.add(post)
    posts = request.user.posts.all()
    return render(request, 'postitApp/HTMX/user_posts.html', {'posts': posts})


""" htmx delete a non image user post """


@login_required()
@require_http_methods(['DELETE'])
def deletepost(request, pk):
    # request.user.posts.remove(pk)
    post = UserPost.objects.get(pk=pk)
    post.delete()
    # request.user.posts.remove(post)
    posts = request.user.posts.all()
    return render(request, 'postitApp/HTMX/user_posts.html', {'posts': posts})


""" Dynamic Searchbar for User Search """


@login_required()
def searchuser(request):
    search_text = request.POST.get('search')
    if not search_text:
        results = ""
        searchbool = False  # Used in order to display 'no results' or not on the template
    else:
        results = CustomUser.objects.filter(username__startswith=search_text)
        searchbool = True
    return render(request, 'postitApp/HTMX/dynamic_user_search_results.html', {'results': results,
                                                                               'searchbool': searchbool})


""" Dogs List - filtered by dogs that don't exist in the user's preferred dogs """


def dogsList(request):
    dogs = dog.objects.filter(user_owns=request.user)
    return render(request, 'postitApp/HTMX/DogsSortedList.html', {'dogs': dogs})


def dogsNotPreferredList(request):
    not_preferred = dog.objects.exclude(user_owns=request.user)
    context = {'not_preferred': not_preferred}
    return render(request, 'postitApp/HTMX/DogsNotPreferred.html', context)


def addDog(request, pk):
    dog_instance = get_object_or_404(dog, id=pk)
    if not userDogPreference.objects.filter(user=request.user, dog=dog_instance).exists():
        userDogPreference.objects.create(user=request.user, dog=dog_instance, order=1)
    response = dogsList(request)
    trigger_client_event(response, 'edited_dog_list', {})
    return response


def deleteAllDogs(request):
    userDogPreference.objects.all().delete()
    response = dogsList(request)
    trigger_client_event(response, 'edited_dog_list', {})
    return response


def suggestedUsers(request, number_results):
    context = generateNotFollowingList(request, number_results=number_results)

    return render(request, 'postitApp/suggested_following.html', context)


def followAndGetNewSuggestedUser(request, pk):
    response = followUser(request, pk)
    context = generateNotFollowingList(request, number_results=1)
    single_user = {'u': context.pop('not_following').first(), 'fq': context.pop('fq')}
    return render(request, 'postitApp/HTMX/Partials/suggested_user.html', single_user)


def updateLikesDisplayed(request, post_id):
    post = UserPost.objects.get(id=post_id)
    t_dict = {post: likesQuery(request, post)}
    context = {'lq': t_dict, 'post': post}
    return render(request, 'postitApp/HTMX/Partials/likes_count.html', context)


def getCommentsForPost(request, post_id):
    post = UserPost.objects.get(id=post_id)
    comments = post.comments.all().order_by('-created')
    context = {'comments': comments}
    return render(request, 'postitApp/HTMX/Partials/post_comments.html', context)


""" ***************************** """
