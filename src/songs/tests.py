from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from songs.models import Song


class SongViewTestCase(APITestCase):
    list_url = reverse_lazy("songs:song-list")

    def tearDown(self) -> None:
        Song.objects.all().delete()

    def test_should_return_list_of_songs(self):
        songs_data = [
            {"title": "Title1", "original_title": "OTitle1", "author": "Author1", "lyrics": "", "order": 1},
            {"title": "Title2", "original_title": "OTitle2", "author": "Author2", "lyrics": "", "order": 2},
        ]

        Song.objects.bulk_create([Song(**song) for song in songs_data])

        response = self.client.get(self.list_url)

        for response_song, expected_song in zip(response.data, songs_data):
            self.assertEqual(response_song["title"], expected_song["title"])

    def test_should_not_allow_to_create_new_song_via_api(self):
        songs_data = {"title": "Title1", "original_title": "OTitle1", "author": "Author1", "lyrics": "", "order": 1}
        response = self.client.post("/api/songs/", songs_data)

        self.assertEqual(response.status_code, 403)
