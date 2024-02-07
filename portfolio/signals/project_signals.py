from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import Project
from ..utils import generate_unique_slug


@receiver(pre_save, sender=Project)
def create_slug_project(sender, instance, *args, **kwargs):
    generate_unique_slug(instance)
