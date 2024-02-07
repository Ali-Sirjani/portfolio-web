from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

from ..abstract import TimestampedModel


class Category(MPTTModel, TimestampedModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    name = models.CharField(unique=True, max_length=200, verbose_name=_('name'))
    slug_change = models.BooleanField(verbose_name=_('slug change'), help_text=_('If you want change the slug by name'))
    slug = models.SlugField(allow_unicode=True, blank=True, max_length=300, verbose_name=_('slug'),
                            help_text=_('If field be empty it\'s automatic change by name '))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return f'{self.name}'


class ActivePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(can_published=True)


class Post(TimestampedModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('category'))

    title = models.CharField(max_length=250, verbose_name=_('title'))
    description = RichTextField(verbose_name=_('description'))
    can_published = models.BooleanField(default=True, verbose_name=_('can published'))
    slug_change = models.BooleanField(verbose_name=_('slug change'), help_text=_('If you want change the slug by name'))
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, max_length=300, verbose_name=_('slug'),
                            help_text=_('If field be empty it\'s automatic change by name '))

    objects = models.Manager()
    active_objs = ActivePostManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return f'{self.title}'


class PostImage(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('post'))

    image = models.ImageField(upload_to='post_images/', verbose_name=_('image'))
    is_main = models.BooleanField(default=False, verbose_name=_('main'))

    class Meta:
        verbose_name = _('post image')
        verbose_name_plural = _('post images')

    def __str__(self):
        return f'{self.post.pk}'


class PostComment(MPTTModel, TimestampedModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', verbose_name=_('post'))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='post_comments',
                               verbose_name=_('author'))

    text = models.TextField(verbose_name=_('text'))

    confirmation = models.BooleanField(default=False, verbose_name=_('confirmation'))

    class Meta:
        verbose_name = _('post comment')
        verbose_name_plural = _('post comments')

    def __str__(self):
        return f'author: {self.author}, post pk: {self.post.pk}'
