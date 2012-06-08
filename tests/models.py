#-*- coding: utf-8 -*-

from django.db import models


class Article(models.Model):

    title = models.CharField("title", max_length=50)

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return self.title
