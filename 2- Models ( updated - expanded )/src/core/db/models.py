from django.utils import timezone
from django.db import models


class BasePublicModel(models.Model):
    class STATE_CHOICES(models.TextChoices):
        PUBLIC = 'PU', 'Public'
        PRIVATE = 'PR', 'Private'

    class Meta:
        abstract = True

    state = models.CharField(
        max_length=120, default=STATE_CHOICES.PRIVATE, choices=STATE_CHOICES.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    time_when_public = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True)

    def save(self, *args, **kwargs):
        if self.is_public and self.time_when_public is None:
            self.time_when_public = timezone.now()
        else:
            self.time_when_public = None
        super().save(*args, **kwargs)

    @property
    def is_public(self):
        return self.state == self.STATE_CHOICES.PUBLIC
