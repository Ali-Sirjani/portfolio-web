from django.db import models
from django.utils.translation import gettext_lazy as _

from ..abstract import TimestampedModel


class ContactMe(TimestampedModel):
    full_name = models.CharField(max_length=100, verbose_name=_('full name'))
    email = models.EmailField(verbose_name=_('email'),)
    subject = models.CharField(max_length=200, verbose_name=_('subject'))
    message = models.TextField(verbose_name=_('message'))
    answer = models.BooleanField(default=False, verbose_name=_('answer'))

    class Meta:
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')

    def __str__(self):
        return f'{self.full_name} - {self.subject}'
