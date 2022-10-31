from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=125)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return f'/detail/{self.slug}/'

    def get_update_url(self):
        return f'/detail/and/update/{self.slug}'

    def get_delete_url(self):
        return f"/product/delete/{self.slug}/"


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


pre_save.connect(slugify_pre_save, sender=Product)

# Proxy


class ProxyProduct(Product):
    class Meta:
        proxy = True
