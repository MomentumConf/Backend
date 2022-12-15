from django.db import models
from markdownfield.models import MarkdownField, RenderedMarkdownField


class Song(models.Model):
    class Meta:
        ordering = ["order"]

    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    lyrics = MarkdownField(rendered_field="rendered_lyrics")
    rendered_lyrics = RenderedMarkdownField()
    order = models.PositiveSmallIntegerField(default=1)
