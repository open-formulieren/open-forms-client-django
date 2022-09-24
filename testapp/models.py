from django.db import models

from openformsclient.models import OpenFormsField


class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    form = OpenFormsField(blank=True)

    def __str__(self):
        return self.title
