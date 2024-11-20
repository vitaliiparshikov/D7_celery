from django.urls import path
from .views import PostListView, PostCreateView, ArticleCreateView, PostUpdateView, PostDeleteView, search, subscribe

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('search/', search, name='post_search'),
    path('news/create/', PostCreateView.as_view(), name='post_create'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('articles/<int:pk>/edit/', PostUpdateView.as_view(), name='article_edit'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='article_delete'),
    path('subscriptions/', subscribe, name='subscriptions'),
]