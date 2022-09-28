from django.urls import path

from . import views
from .views import indexView

urlpatterns = [
    #path('', views.index, name='index'),
    path('', indexView.as_view(), name='index'),
    path('landing/', views.landingPage, name='landing-page'),
    path('about/', views.aboutPage, name='about'),
    path('login/', views.loginUser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('edit_user/', views.editUser, name='edit-user'),
    path('logout/', views.logoutUser, name='logout'),
    path('new_post/', views.newPost.as_view(), name='create_post'),
    path('new_post_submit/', views.new_post_submit, name='new-post-submit'),
    # path('delete_post <str:pk> /', views.delete_post, name='delete-post')
    path('delete_post <str:pk> /', views.deletePost.as_view(), name='delete-post')
]

