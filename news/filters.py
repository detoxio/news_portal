from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter, BooleanFilter
from .models import Post, Author, Category, User


class PostFilter(FilterSet):
    headline = CharFilter('headline',
                          label='Заголовок содержит:',
                          lookup_expr='icontains', )

    content = CharFilter('content',
                         label='Текст содержит:',
                         lookup_expr='icontains',
                         )

    author_post = ModelChoiceFilter(field_name='author_post',
                                    label='Автор:',
                                    lookup_expr='exact',
                                    queryset=Author.objects.all()
                                    )
    categories = ModelChoiceFilter(field_name='categories',
                                   label='Категория:',
                                   lookup_expr='exact',
                                   queryset=Category.objects.all()
                                   )
    time_create = DateFilter(
        field_name='time_create',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Дата публикации:'
    )

    class Meta:
        model = Post
        fields = []


class CategoryFilter(FilterSet):
    name = ModelChoiceFilter(field_name='name',
                             label='Выберите категорию новостей:',
                             lookup_expr='exact',
                             queryset=Category.objects.all()
                             )

    check_box = BooleanFilter(field_name='check_box',
                              label='Даю согласие на отправку подборки по email')


    class Meta:
        model = Category
        fields = []