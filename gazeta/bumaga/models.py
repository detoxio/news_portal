from django.db import models
from django.contrib.auth.models import User

article = "AR"
news = "NW"

POST_TYPES = [
    (article, "Статья"),
    (news, "Новость")
]


class Author(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.user_rating = 0
        for post in Post.objects.filter(author_name=self):
            self.user_rating += post.post_rating * 3
            for comment in Comment.objects.filter(comment_post=post):
                self.user_rating += comment.comment_rating
        for comment in Comment.objects.filter(comment_user=self.user_name):
            self.user_rating += comment.comment_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through="PostCategory")
    post_header = models.CharField(max_length=50)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        self.post_text = self.post_text[0:125] + "..."
        self.save()

    def like(self, amount=0):
        self.post_rating += amount
        self.save()

    def dislike(self, amount=0):
        self.post_rating -= amount
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=255)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self, amount=0):
        self.comment_rating += amount
        self.save()

    def dislike(self, amount=0):
        self.comment_rating -= amount
        self.save()

