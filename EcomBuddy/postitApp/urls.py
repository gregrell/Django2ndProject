from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_post/', views.new_post, name='create_post')
]

