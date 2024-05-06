from django.db import models
from django.template.defaultfilters import truncatewords
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from meta.models import ModelMeta

from ..abstract import TimestampedModel


class Category(MPTTModel, TimestampedModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    name = models.CharField(unique=True, max_length=200, verbose_name=_('name'))
    slug_change = models.BooleanField(verbose_name=_('slug change'), help_text=_('If you want change the slug by name'))
    slug = models.SlugField(allow_unicode=True, blank=True, max_length=300, verbose_name=_('slug'),
                            help_text=_('If field be empty it\'s automatic change by name'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('portfolio:post_category_list', args=[self.slug])


class TopCategory(TimestampedModel):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )

    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='top_categories',
                                    verbose_name=_('category'))

    level = models.CharField(max_length=1, choices=LEVEL_CHOICES,
                             help_text=_('Levels are ordered from top to bottom, with 1 being the highest.'),
                             verbose_name=_('level'))
    is_top_level = models.BooleanField(default=False,
                                       help_text='Check this box if you want the category to be at the top of its specified level.',
                                       verbose_name='is_top_level')

    class Meta:
        verbose_name = _('top category')
        verbose_name_plural = _('top categories')

    def __str__(self):
        return f'{self.category}'


class ActivePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(can_published=True)


class Post(ModelMeta, TimestampedModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='posts', null=True, blank=True,
                                 verbose_name=_('category'))

    title = models.CharField(max_length=250, verbose_name=_('title'))
    description = RichTextField(verbose_name=_('description'))
    can_published = models.BooleanField(default=True, verbose_name=_('can published'))
    keywords = models.CharField(max_length=250, blank=True, verbose_name=_('keywords'),
                                help_text=_(
                                    'Keywords for SEO (separated by #). Category name will be automatically added.'
                                ))

    slug_change = models.BooleanField(verbose_name=_('slug change'), help_text=_('If you want change the slug by name'))
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, max_length=300, verbose_name=_('slug'),
                            help_text=_('If field be empty it\'s automatic change by title'))

    objects = models.Manager()
    active_objs = ActivePostManager()

    _metadata = {
        'title': 'title',
        'description': 'get_description_metadata',
        'keywords': 'get_keywords_as_list',
        'image': 'main_image_url',
        'image_width': 600,
        'image_height': 600,
        'url': 'get_absolute_url',
        'modified_time': 'datetime_updated',
        'locale': 'fa_IR',
    }

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('portfolio:post_detail', args=[self.slug])

    def main_image_url(self):
        for image in self.images.all():
            if image.is_main:
                return image.image.url

        return None

    def get_description_metadata(self):
        return truncatewords(strip_tags(self.description), 20)

    def get_keywords_as_list(self):
        keywords_list = [keyword.strip() for keyword in self.keywords.split('#') if keyword.strip()]

        if self.category:
            keywords_list.append(self.category.name)

        return keywords_list


class PostImage(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name=_('post'))

    image = models.ImageField(upload_to='post_images/', verbose_name=_('image'))
    is_main = models.BooleanField(default=False, verbose_name=_('main'))

    class Meta:
        verbose_name = _('post image')
        verbose_name_plural = _('post images')
        ordering = ('-is_main',)

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
