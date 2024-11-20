from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Post  # Используется модель Post
from .filters import PostFilter
from django.utils import timezone

from .tasks import send_new_post_notification  # использование Celery для рассылки уведомлений

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SubscriptionForm
from .models import Subscriber

def index(request):
    latest_articles = Post.objects.filter(post_type='article').order_by('-pub_date')[:10]
    return render(request, 'news/index.html', {'latest_articles': latest_articles})

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'news/detail.html', {'post': post})

class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'news/post_list.html'
    context_object_name = 'posts'

def search(request):
    post_filter = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'news/post_search.html', {'filter': post_filter})

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'news/post_form.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.pub_date = timezone.now()
        post.save()
        send_new_post_notification.delay(post.id)  # Запуск задачи Celery
        return super().form_valid(form)

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'news/post_form.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        post.pub_date = timezone.now()
        post.save()
        send_new_post_notification.delay(post.id)  # Запуск задачи Celery
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'news/post_form.html'
    permission_required = ('news.change_post',)

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)


@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('subscriptions')
    else:
        form = SubscriptionForm(user=request.user)
    return render(request, 'news/subscriptions.html', {'form': form})
