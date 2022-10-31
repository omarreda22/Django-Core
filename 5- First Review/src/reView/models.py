from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


class ViewBlog(models.Model):
    title = models.CharField(max_length=125)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.title


def slugify_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug or instance.slug == '':
        new_slug = slugify(instance.title)
        klass = instance.__class__
        qs = klass.objects.filter(
            slug__icontains=new_slug).exclude(id=instance.id)
        if qs.count() == 0:
            instance.slug = new_slug
        else:
            instance.slug = f"{new_slug}-{qs.count()}"


pre_save.connect(slugify_pre_save, sender=ViewBlog)
