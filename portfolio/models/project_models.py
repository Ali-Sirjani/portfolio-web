from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract import TimestampedModel


class ProjectActiveManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Project(TimestampedModel):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    client = models.CharField(max_length=255, blank=True, verbose_name=_('client'))
    link = models.URLField(blank=True, verbose_name=_('link'))
    location = models.TextField(blank=True, verbose_name=_('location'))
    start_date = models.DateField(verbose_name=_('start date'))
    slug_change = models.BooleanField(verbose_name=_('slug change'), help_text=_('If you want change the slug by name'))
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, max_length=300, verbose_name=_('slug'),
                            help_text=_('If field be empty it\'s automatic change by title'))

    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    objects = models.Manager()
    active_objs = ProjectActiveManger()

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return f'{self.title}'

    def main_image_url(self):
        for image in self.images.all():
            if image.is_main:
                return image.image.url

        return None


class ProjectImage(TimestampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name=_('project'))

    image = models.ImageField(upload_to='project_images/', verbose_name=_('image'))
    is_main = models.BooleanField(default=False, verbose_name=_('main'))

    class Meta:
        verbose_name = _('project image')
        verbose_name_plural = _('project images')
        ordering = ('-is_main', )

    def __str__(self):
        return f'{self.project.pk}'
