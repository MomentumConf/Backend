from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join

from speeches.models import Speaker, Topic


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "priority", "image")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_date", "finish_date", "speaker_list")

    @admin.display(description="Mówcy")
    def speaker_list(self, obj: Topic):
        speakers = obj.speakers.all()

        def prepare_speaker_link(speaker: Speaker):
            return (
                reverse("admin:speeches_speaker_change", args=(speaker.pk,)),
                speaker.name,
            )

        return format_html_join(
            ", ",
            '<a href="{}">{}</a>',
            (prepare_speaker_link(speaker) for speaker in speakers),
        )
