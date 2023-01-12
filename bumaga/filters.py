import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post


class NewsFilter(FilterSet):
    post_date = django_filters.DateFilter(
        lookup_expr='gt',
        label='Не раньше, чем',
        widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'post_header': ['icontains'],
            'post_text': ['icontains'],
            }