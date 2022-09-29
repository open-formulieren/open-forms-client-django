from django.db import models

from openformsclient.models import OpenFormsSlugField, OpenFormsUUIDField


class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    form_slug = OpenFormsSlugField(blank=True)
    form_uuid = OpenFormsUUIDField(blank=True, null=True)

    def __str__(self):
        return self.title
