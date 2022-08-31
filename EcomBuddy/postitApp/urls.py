from django.urls import path

from . import views
from .views import indexView

urlpatterns = [
    #path('', views.index, name='index'),
    path('', indexView.as_view(), name='index'),
    #path('new_post/', views.new_post, name='create_post'),
    path('new_post/',views.newPost.as_view(), name='create_post'),
    path('new_post_submit/', views.new_post_submit, name='new-post-submit'),
    # path('delete_post <str:pk> /', views.delete_post, name='delete-post')
    path('delete_post <str:pk> /', views.deletePost.as_view(), name='delete-post')
]

