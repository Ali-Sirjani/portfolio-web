from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ..abstract import TimestampedModel


class ContactMe(TimestampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='messages', blank=True,
                             null=True, verbose_name=_('user'))

    full_name = models.CharField(max_length=100, verbose_name=_('full name'))
    email = models.EmailField(verbose_name=_('email'), )
    subject = models.CharField(max_length=200, verbose_name=_('subject'))
    message = models.TextField(verbose_name=_('message'))
    answer = models.BooleanField(default=False, verbose_name=_('answer'))

    class Meta:
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')

    def __str__(self):
        return f'{self.full_name} - {self.subject}'
