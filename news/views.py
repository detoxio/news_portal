from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Author, Category, PostCategory, User
from .filters import PostFilter, CategoryFilter
from datetime import datetime, timedelta
from .forms import PostForm, CategoryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse

from celery.utils.log import get_logger

logger = get_logger(__name__)


# Create your views here.


class PostList(ListView):
    queryset = Post.objects.all().order_by('-time_create')
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        context['filterset'] = self.filterset
        return context




class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post_detail'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_edit')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_delete')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts')


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_edit')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class Subscribe(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'subscribe.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CategoryFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CategoryFilter(self.request.GET, queryset=self.get_queryset())
        context['name'] = Category.objects.all()
        context['form'] = CategoryForm()
        context['filterset'] = self.filterset

        return context

    def post(self, request, **kwargs):
        subscriber = request.user
        category = Category.objects.get(pk=request.POST['name'])
        category.subscribers.add(subscriber)
        return redirect('/accounts/profile/')