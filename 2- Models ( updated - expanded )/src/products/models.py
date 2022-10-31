from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .validators import block
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CustomQuerySet(models.QuerySet):
    # Product.objects.all().published_products()
    # Product.objects.published().published_products()
    def published_products(self):
        now = timezone.now()
        return self.filter(state=Product.STATE_CHOICES.PUBLIC, time_when_public__lte=now)


class CustomProductManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    # Product.objects.published()
    def published(self):
        return self.get_queryset().published_products()


class Product(models.Model):
    class STATE_CHOICES(models.TextChoices):
        PUBLIC = 'PU', 'Public'
        PRIVATE = 'PR', 'Private'

    title = models.CharField(max_length=120)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # blank --> You can let her empty, null --> Can Data be empty
    slug = models.SlugField(blank=True, null=True, db_index=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    state = models.CharField(
        max_length=120, default=STATE_CHOICES.PRIVATE, choices=STATE_CHOICES.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    time_when_public = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True)

    objects = CustomProductManager()

    def save(self, *args, **kwargs):
        block(self.title)
        block(self.description)
        if self.is_public and self.time_when_public is None:
            self.time_when_public = timezone.now()
        else:
            self.time_when_public = None
        super().save(*args, **kwargs)

    @property
    def is_public(self):
        return self.state == self.STATE_CHOICES.PUBLIC

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'
        unique_together = [['title', 'description']]
        # db_table = 'music_album'


def slugify_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None or instance.slug == '':
        new_slug = slugify(instance.title)
        klass = instance.__class__
        qs = klass.objects.filter(
            slug__icontains=new_slug).exclude(id=instance.id)
        if qs.count() == 0:
            instance.slug = new_slug
        else:
            instance.slug = f'{new_slug}-{qs.count()}'


pre_save.connect(slugify_pre_save, sender=Product)
