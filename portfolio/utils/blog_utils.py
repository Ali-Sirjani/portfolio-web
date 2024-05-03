from django.db.models import Count

from ..models import TopCategory, Category


def top_category_query():
    category_pk_list = TopCategory.objects.values_list('category__pk')
    category_queryset = Category.objects.filter(pk__in=category_pk_list).annotate(post_count=Count('posts'))
    return category_queryset.order_by('top_categories__level', '-top_categories__is_top_level')
