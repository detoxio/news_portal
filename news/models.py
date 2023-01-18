from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms



class Status(models.TextChoices):
    POST = 'PO', 'Post'
    NEWS = 'NE', 'News'


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_rate = models.IntegerField(default=0)

    def update_rating(self):
        self.user_rate = 0
        self.total_com_rate = 0
        self.total_post_rate = 0
        self.total_comment = 0
        for comment_iter in Comment.objects.filter(comment_aut=self.author_user):
            self.total_com_rate = self.total_com_rate + comment_iter.comment_rate
        for post_iter in Post.objects.filter(author_post=self.author_user_id):
            self.total_post_rate = self.total_post_rate + post_iter.post_rate
            for comment_iter in Comment.objects.filter(post_com=post_iter):
                self.total_comment = self.total_comment + comment_iter.comment_rate
        self.user_rate = (self.total_post_rate * 3) + self.total_com_rate + self.total_comment
        self.save()

    def __str__(self):
        return f'{self.author_user}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, max_length=200, blank=True)

    def __str__(self):
        return f'{self.name}'




class Post(models.Model):
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.POST)
    time_create = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=255)
    content = models.TextField()
    post_rate = models.IntegerField(default=0)

    def like(self, amount=1):
        self.post_rate += amount
        self.save()

    def dislike(self, amount=1):
        self.post_rate -= amount
        self.save()

    def preview(self):
        self.content = self.content[0:125] + '...'
        return f'Заголовок:{self.headline}, Текст: {self.content}'

    def __str__(self):
        return f'{self.content}'

    def get_absolute_url(self):
        return f'{self.id}'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_com = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_aut = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like(self, amount=1):
        self.comment_rate += amount
        self.save()

    def dislike(self, amount=1):
        self.comment_rate -= amount
        self.save()


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)