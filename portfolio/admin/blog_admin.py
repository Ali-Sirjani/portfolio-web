from django.contrib import admin
from django.db.models import Count
from django.utils.http import urlencode
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator

from mptt.admin import MPTTModelAdmin

from ..models import Category, TopCategory, PostImage, Post, PostComment
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


@admin.register(TopCategory)
class TopCategoryAdmin(admin.ModelAdmin):
    fields = ('category', 'level', 'is_top_level', 'datetime_created', 'datetime_updated',)
    readonly_fields = ('datetime_created', 'datetime_updated',)
    autocomplete_fields = ('category',)
    list_display = ('category', 'level', 'is_top_level')
    ordering = ('level', '-is_top_level')
    search_fields = ('category__name',)


class PostImageTabu(admin.TabularInline):
    model = PostImage
    formset = PostImageTabuFormSetAdmin
    fields = ('image', 'is_main',)
    extra = 1
    min_num = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Post Information'), {
            'fields': ('title', 'description', 'category', 'keywords', 'can_published')
        }),
        (_('Slug Settings'), {
            'classes': ('collapse',),
            'fields': ('slug_change', 'slug')
        }),
        (_('Date and Time'), {
            'classes': ('collapse',),
            'fields': ('datetime_created', 'datetime_updated'),
        }),
    )
    readonly_fields = ('datetime_created', 'datetime_updated')
    autocomplete_fields = ('category', )
    list_display = ('limit_title', 'can_published', 'datetime_created', 'datetime_updated')
    inlines = (PostImageTabu, )
    search_fields = ('title', )
    list_filter = ('can_published', )
    ordering = ('-datetime_updated',)

    def limit_title(self, obj):
        return Truncator(obj.title).words(15)


@admin.register(PostComment)
class PostCommentAdmin(MPTTModelAdmin):
    fields = ('post', 'author', 'parent', 'text', 'confirmation',
              'datetime_created', 'datetime_updated',)
    list_display = ('author', 'limit_text', 'confirmation', 'datetime_updated',)
    autocomplete_fields = ('post', 'author')
    list_filter = ('confirmation',)
    search_fields = ('pk', 'post__title')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['datetime_created', 'datetime_updated', ]
        if obj:
            readonly_fields.extend(['post', 'author'])

        return readonly_fields

    def limit_text(self, obj):
        return Truncator(obj.text).words(15)
