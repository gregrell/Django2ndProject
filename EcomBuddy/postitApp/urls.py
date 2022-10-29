from django.urls import path

from . import views
from .views import indexView

urlpatterns = [
    # path('', views.index, name='index'),
    path('', indexView.as_view(), name='index'),
    path('landing/', views.landingPage, name='landing-page'),
    path('about/', views.aboutPage, name='about'),
    path('login/', views.loginUser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('edit_user/', views.editUser, name='edit-user'),
    path('public_profile/<str:pk>/', views.publicProfile, name='public-profile'),
    path('logout/', views.logoutUser, name='logout'),
    path('new_post/', views.newPost.as_view(), name='create_post'),
    path('new_post_submit/', views.new_post_submit, name='new-post-submit'),
    # path('delete_post <str:pk> /', views.delete_post, name='delete-post')
    path('delete_post <str:pk> /', views.deletePost.as_view(), name='delete-post'),
    path('unfollow_user <str:pk> /', views.unfollowUser, name='unfollow-user'),
    path('follow_user <str:pk> /', views.followUser, name='follow-user'),
    path('like_post <str:post_id> /', views.likePost, name='like-post')
]

htmxpatterns = [
    path('play/', views.htmxPlay, name='htmxplay'),
    path('check_username/', views.checkUsername, name='check-username'),
    path('createnoimagepost/', views.createnoimagepost, name='createnoimagepost'),
    path('deletepost <int:pk>/', views.deletepost, name='deletepost'),
    path('searchuser/', views.searchuser, name='search-user')

]

urlpatterns += htmxpatterns
