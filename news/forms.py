from django.forms import ModelForm, BooleanField
from .models import Post, Category


class PostForm(ModelForm):
    check_box = BooleanField(label='Готово')

    class Meta:
        model = Post
        fields = ['status', 'headline', 'content', 'author_post', 'categories', 'check_box']


class CategoryForm(ModelForm):
    check_box = BooleanField(label='Даю согласие на рассылку по email')

    class Meta:
        model = Category
        fields = ['name', 'subscribers', 'check_box']