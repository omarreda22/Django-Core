from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

from reView.models import slugify_pre_save
from .validation import not_omar_in, blocks


class CustomQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(active=True)


class CustomMainManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def is_private_manager(self):
        return self.filter(active=True)


class Main(models.Model):
    class STATE_CHOICES(models.TextChoices):
        PUBLIC = 'PU', 'Public'
        PRIVATE = 'PR', 'Private'

    title = models.CharField(max_length=125, validators=[
                             not_omar_in, blocks])
    slug = models.SlugField(unique=True, blank=True)
    descrip = models.TextField(blank=True)
    state = models.CharField(
        max_length=25, default=STATE_CHOICES.PUBLIC, choices=STATE_CHOICES.choices)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    when_public = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True, blank=True)
    objects = CustomMainManager()

    def __str__(self):
        return self.title

    @property
    def is_private(self):
        return self.state == self.STATE_CHOICES.PRIVATE

    class Meta:
        ordering = ['-updated', '-create']
        verbose_name = 'Blogs'
        verbose_name_plural = 'Model Blogs'

    def save(self, *args, **kwargs):
        if not self.is_private and self.when_public == None:
            self.when_public = timezone.now()
            self.active = True
        else:
            self.when_public = None
            self.active = False

        # if self.slug is None or self.slug == '':
        #     self.slug = slugify(self.title)

        blocks(self.title)
        super().save(*args, **kwargs)

    # create after class based view
    def get_absolute_url(self):
        return f'/cbv/detail/{self.slug}'


def second_slugify(sender, instance, *args, **kwargs):
    if instance.slug is None or instance.slug == '':
        new_slug = slugify(instance.title)
        klass = instance.__class__
        qs = klass.objects.filter(
            slug__icontains=new_slug).exclude(id=instance.id)
        if qs.count() == 0:
            instance.slug = new_slug
        else:
            instance.slug = f'{new_slug}-{qs.count()}'


pre_save.connect(second_slugify, sender=Main)


# pre_save.connect(slugify_pre_save, sender=Main)
