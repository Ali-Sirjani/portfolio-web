from django.contrib import admin
from django.db.models import Count
from django.utils.http import urlencode
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator

from mptt.admin import MPTTModelAdmin

from ..models import Category, PostImage, Post, PostComment
from ..forms import PostImageTabuFormSetAdmin


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'post_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(post_count=Count('posts'))

    def post_count(self, obj):
        url = (reverse('admin:portfolio_post_changelist') + '?' + urlencode({'category': obj.pk}))
        return format_html('<a href="{}">{}</a>', url, obj.post_count)


class PostImageTabu(admin.TabularInline):
    model = PostImage
    formset = PostImageTabuFormSetAdmin
    fields = ('image', 'is_main',)
    extra = 1
    min_num = 1
