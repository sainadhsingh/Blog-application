from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('category/<slug:slug>/', views.PostListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.PostListView.as_view(), name='tag_posts'),
    
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/like/', views.LikePostView.as_view(), name='post_like'),
    path('post/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),

    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # RSS Feed
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
