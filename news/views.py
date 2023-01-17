import os
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, CategorySubscribers
from .forms import NewsForm, SubscribeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .filters import NewsFilter
from dotenv import load_dotenv, find_dotenv
from django.contrib.auth.models import User

load_dotenv(find_dotenv())


@receiver(post_save, sender=Post)
def notify_category_subscribers(sender, instance, created=True, **kwargs):
    send_mail(
        subject="You have new posts in subscriptions",
        message=Post.post_text[:50],
        from_email=os.environ.get('EMAIL')+'yandex.ru',
        recipient_list=User.email
    )


class NewsList(ListView):
    queryset = Post.objects.all().order_by().values()
    ordering = 'post_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsSearch(ListView):
    queryset = Post.objects.all().order_by().values()
    ordering = 'post_date'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NW'
        return super().form_valid(form)


class NewsSubscribe(CreateView):
    form_class = SubscribeForm
    model = CategorySubscribers
    template_name = 'subscribe.html'


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.update_post')
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.update_post')
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')