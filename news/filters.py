import django_filters
from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post

class PostFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    created_after = DateTimeFilter(
        field_name='pub_date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'created_after']