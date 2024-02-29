from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from portfolio.abstract import TimestampedModel


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, verbose_name=_('email'))


class Profile(TimestampedModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile',
                                verbose_name=_('user'))

    first_name = models.CharField(max_length=200, blank=True, verbose_name=_('First name'))
    last_name = models.CharField(max_length=200, blank=True, verbose_name=_('Last name'))
    picture = models.ImageField(upload_to='profile_pictures/',
                                default='../static/images/logo-icon.png', blank=True,
                                verbose_name=_('picture'))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return f'{self.user.username}'
