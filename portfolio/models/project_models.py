from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.shortcuts import reverse
from django.template.defaultfilters import truncatechars

from urllib.parse import urlparse
from meta.models import ModelMeta

from ..abstract import TimestampedModel


class ProjectActiveManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Project(ModelMeta, TimestampedModel):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    client = models.CharField(max_length=255, blank=True, verbose_name=_('client'))
    link = models.URLField(blank=True, verbose_name=_('link'))
    location = models.TextField(blank=True, verbose_name=_('location'))
    start_date = models.DateField(verbose_name=_('start date'))
    video = models.FileField(upload_to='project_videos/', null=True, blank=True,
                             validators=[
                                 FileExtensionValidator(
                                     allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv'],
                                     message=_(
                                         'Unsupported file format. Please upload a .MOV, .AVI, .MP4, .WEBM, or .MKV file.')
                                 ),
                             ],
                             verbose_name=_('video')
                             )
    keywords = models.CharField(max_length=500, blank=True, verbose_name=_('keywords'),
                                help_text=_(
                                    'Keywords for SEO (separated by #). Category name will be automatically added.'
                                ))

    slug_change = models.BooleanField(verbose_name=_('slug change'), help_text=_('If you want change the slug by name'))
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, max_length=300, verbose_name=_('slug'),
                            help_text=_('If field be empty it\'s automatic change by title'))

    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    objects = models.Manager()
    active_objs = ProjectActiveManger()

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
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', args=[self.slug])

    def main_image_url(self):
        for image in self.images.all():
            if image.is_main:
                return image.image.url

        return None

    def get_description_metadata(self):
        return truncatechars(self.description, 155)

    def get_keywords_as_list(self):
        return [keyword.strip() for keyword in self.keywords.split('#') if keyword.strip()]

    def display_domain_link(self):
        parsed_url = urlparse(self.link)
        return parsed_url.netloc


class ProjectImage(TimestampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name=_('project'))

    image = models.ImageField(upload_to='project_images/', verbose_name=_('image'))
    is_main = models.BooleanField(default=False, verbose_name=_('main'))

    class Meta:
        verbose_name = _('project image')
        verbose_name_plural = _('project images')
        ordering = ('-is_main',)

    def __str__(self):
        return f'{self.project.pk}'
