from django.urls import path, include
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('about/', include('about.urls', namespace='about')),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit', views.post_edit, name='post_edit'),


]
