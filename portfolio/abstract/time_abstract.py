from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('datetime created'), )
    datetime_updated = models.DateTimeField(auto_now=True, verbose_name=_('datetime updated'), )

    class Meta:
        abstract = True
