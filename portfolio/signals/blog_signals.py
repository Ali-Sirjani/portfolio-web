from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import Post, Category
from ..utils import generate_unique_slug


@receiver(pre_save, sender=Post)
def create_slug_project(sender, instance, *args, **kwargs):
    generate_unique_slug(instance)


@receiver(pre_save, sender=Category)
def create_slug_category(sender, instance, *args, **kwargs):
    generate_unique_slug(instance)
