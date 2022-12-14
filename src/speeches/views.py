from rest_framework import viewsets

from speeches.models import Speaker, Topic
from speeches.serializers import SpeakerSerializer, TopicSerializer


class SpeakerView(viewsets.ReadOnlyModelViewSet):
    queryset = Speaker.objects.filter(priority__gt=0).order_by("-priority")
    serializer_class = SpeakerSerializer


class TopicView(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.prefetch_related("speakers").filter(priority__gt=0).order_by("start_date", "-priority")
    serializer_class = TopicSerializer
