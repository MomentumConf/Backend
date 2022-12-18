from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import mark_safe
from .models import Song


@admin.register(Song)
class SongAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("order", "title", "original_title", "full_lyrics")

    def full_lyrics(self, obj: Song):
        return mark_safe(obj.rendered_lyrics)
