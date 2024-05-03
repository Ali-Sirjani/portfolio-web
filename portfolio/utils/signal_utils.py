import random

from django.utils.text import slugify


def create_unique_slug(instance, create_by, slug_primitive=None):
    if instance.slug_change or slug_primitive is None:
        slug = slugify(create_by, allow_unicode=True)
    else:
        slug = slug_primitive

    ins_class = instance.__class__
    objs = ins_class.objects.filter(slug=slug)

    if objs.exists():
        if objs.count() == 1 and instance.pk == objs.first().pk:
            return instance.slug
        instance.slug_change = False
        slug = f'{slug}-{random.choice("12345")}'
        return create_unique_slug(instance, create_by, slug)

    return slug


def generate_unique_slug(instance, create_by, slug):
    """
    Generates a unique slug for the given instance.
    """
    if not instance.slug or instance.slug_change:
        instance.slug = create_unique_slug(instance, create_by)
        instance.slug_change = False
    else:
        instance.slug = create_unique_slug(instance, slug)
        instance.slug_change = False
