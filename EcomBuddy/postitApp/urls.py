from django.urls import path

from . import views
from .views import IndexView

urlpatterns = [
    # path('', views.index, name='index'),
    path('', IndexView.as_view(), name='index'),
    path('landing/', views.landingPage, name='landing-page'),
    path('about/', views.aboutPage, name='about'),
    path('login/', views.loginUser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('edit_user/', views.editUser, name='edit-user'),
    path('public_profile/<str:pk>/', views.publicProfile, name='public-profile'),
    path('logout/', views.logoutUser, name='logout'),
    path('new_post/', views.NewPost.as_view(), name='create_post'),
    path('new_post_submit/', views.new_post_submit, name='new-post-submit'),
    # path('delete_post <str:pk> /', views.delete_post, name='delete-post')
    path('delete_post <str:pk> /', views.DeletePost.as_view(), name='delete-post'),
    path('unfollow_user <str:pk> /', views.unfollowUser, name='unfollow-user'),
    path('follow_user <str:pk> /', views.followUser, name='follow-user'),
]

htmxpatterns = [
    path('play/', views.htmxPlay, name='htmxplay'),
    path('check_username/', views.checkUsername, name='check-username'),
    path('createnoimagepost/', views.createnoimagepost, name='createnoimagepost'),
    path('deletepost <int:pk>/', views.deletepost, name='deletepost'),
    path('searchuser/', views.searchuser, name='search-user'),
    path('dogsList/', views.dogsList, name='dogs-list'),
    path('dogsNotPreferredList/', views.dogsNotPreferredList, name='dogs-notpreferred-list'),
    path('addDog <str:pk>/', views.addDog, name='add-dog'),
    path('deletealldogs/', views.deleteAllDogs, name='delete-all-dogs'),
    path('suggestedusers <int:number_results>/', views.suggestedUsers, name='suggested-users'),
    path('followandgetnewsuggesteduser <str:pk>/', views.followAndGetNewSuggestedUser,
         name='follow-and-get-new-suggested-user'),
    path('like_post <str:post_id> /', views.likePost, name='like-post'),
    path('get_likes_count <str:post_id> /', views.updateLikesDisplayed, name='get-likes-count'),
    path('get_comments_for_post <str:post_id> /', views.getCommentsForPost, name='get-comments-for-post')

]

alpinepatterns = [
    path('alpineplay/', views.alpinePlay, name='alpineplay')
]

urlpatterns += htmxpatterns
urlpatterns += alpinepatterns
