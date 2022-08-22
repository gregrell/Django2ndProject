from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_post/', views.new_post, name='create_post'),
    path('new_post_submit/', views.new_post_submit, name='new-post-submit'),
    path('delete_post <str:pk> /', views.delete_post, name='delete-post')
]

