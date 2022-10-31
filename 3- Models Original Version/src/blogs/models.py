from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince
from datetime import datetime, time, timedelta

from .validators import validate_for_email, validate_for_omar

# from django.db.models import Model
# from django.utils.encoding import smart_str

# null => Empty in db
# blank => empty when you input fileds
# This Do automatic by django
# id = models.AutoField(primary_key=True) # Whis will increasing by default 1, 2, 3, 4 , ...

# Custome QuerySet


class CustomeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def title_s(self):
        return self.filter(title__icontains='s')


class BlogManager(models.Manager):
    def get_queryset(self):
        return CustomeQuerySet(self.model, using=self._db)

    # def all(self, *args, **kwargs):
    #     qs = super(BlogManager, self).all(*args, **kwargs).filter(active=True)
    #     # print(qs)
    #     return qs


class Blog(models.Model):
    class STATE_CHOICES(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLIC = 'PU', 'Public'
        PRIVATE = 'PR', 'Private'

    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=125,
        help_text='Must Be uniquq',
        error_messages={
            'unique': 'Please Put this unique',
        }

    )
    slug = models.SlugField(blank=True, null=True)
    descrip = models.TextField(blank=True, verbose_name='Description')
    state = models.CharField(
        max_length=120, default=STATE_CHOICES.DRAFT, choices=STATE_CHOICES.choices)
    active = models.BooleanField(default=False)
    view_count = models.IntegerField(default=1)
    publish_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, default=timezone.now)
    validate = models.CharField(max_length=125, validators=[
                                validate_for_email, validate_for_omar], null=True, blank=True, unique=True)

    objects = BlogManager()
    items = BlogManager()

    def save(self, *args, **kwargs):
        publish_time = datetime.combine(
            self.publish_date, self.publish_date.time())
        print(datetime.now().time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.state == self.STATE_CHOICES.PUBLIC

    @property
    def age(self):
        if self.state == self.STATE_CHOICES.PUBLIC:
            now = datetime.now()
            publish_time = datetime.combine(
                self.publish_date, self.publish_date.time())
            try:
                different = now - publish_time
            except:
                return "Unknown"

            minn = publish_time + timedelta(hours=2)

            if timesince(minn) <= str('0\xa0minutes'):
                return 'just now'
            # print(timesince(minn))
            return f"{timesince(minn).split(', ')[0]} ago"
        else:
            return "not published"


# Before Save Method run
def pre_save_sginals_test(sender, instance, *args, **kwargs):
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_sginals_test, sender=Blog)


# After Save Method Run
def post_save_sginals_test(sender, instance, created, *args, **kwargs):
    if not instance.slug and instance.title:
        instance.slug = f"{slugify(instance.title)}-its-after-save"
        instance.save()


post_save.connect(post_save_sginals_test, sender=Blog)
