from django.contrib import admin
from django.utils.html import mark_safe
from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "original_title", "order", "full_lyrics")

    def full_lyrics(self, obj: Song):
        return mark_safe(obj.rendered_lyrics)
