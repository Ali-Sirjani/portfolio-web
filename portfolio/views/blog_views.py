from django.views import generic
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from ..models import Post, PostComment, TopCategory, Category
from ..forms import PostSearchForm, PostCommentForm


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'portfolio/blog/post_list.html'
    paginate_by = 1

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        if category_slug:
            queryset = Post.active_objs.filter(category__slug=category_slug)

        else:
            queryset = Post.active_objs.all()

        queryset = queryset.order_by('-datetime_updated')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_pk_list = TopCategory.objects.values_list('category__pk')
        category_queryset = Category.objects.filter(pk__in=category_pk_list).annotate(post_count=Count('posts'))
        context['top_categories'] = category_queryset.order_by('top_categories__level', '-top_categories__is_top_level')

        return context
