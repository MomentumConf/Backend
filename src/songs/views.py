from django.shortcuts import render
from rest_framework import viewsets
from songs.models import Song

from songs.serializers import SongSerializer


class SongView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.order_by("order")
