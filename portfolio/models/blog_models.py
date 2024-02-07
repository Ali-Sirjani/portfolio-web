from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

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
