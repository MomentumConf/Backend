from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from speeches.models import Speaker


class SpeakerViewTestCase(APITestCase):
    list_url = reverse_lazy("speeches:speaker-list")

    def tearDown(self) -> None:
        Speaker.objects.all().delete()
        return super().tearDown()

    def test_should_return_list_of_speakers(self):
        speakers_data = [
            {"name": "Speaker1", "description": "Description1", "image": "uploads/speakers/1.jpg"},
            {"name": "Speaker2", "description": "Description2", "image": "uploads/speakers/2.jpg"},
        ]

        Speaker.objects.bulk_create([Speaker(**speaker) for speaker in speakers_data])

        response = self.client.get(self.list_url)

        for response_speaker, expected_speaker in zip(response.data, speakers_data):
            self.assertEqual(response_speaker["name"], expected_speaker["name"])

    def test_should_return_list_in_a_valid_order(self):
        speakers_data = [
            {"name": "Speaker1", "description": "Description1", "image": "uploads/speakers/1.jpg", "priority": 1},
            {"name": "Speaker2", "description": "Description2", "image": "uploads/speakers/2.jpg", "priority": 2},
        ]

        Speaker.objects.bulk_create([Speaker(**speaker) for speaker in speakers_data])

        response = self.client.get(self.list_url)

        self.assertEqual(response.data[0]["name"], speakers_data[1]["name"])
        self.assertEqual(response.data[1]["name"], speakers_data[0]["name"])

    def test_should_not_show_speaker_with_priority_0(self):
        Speaker.objects.create(name="Speaker1", description="Description1", image="uploads/speakers/1.jpg", priority=0)

        response = self.client.get(self.list_url)

        self.assertEqual(response.data, [])
        self.assertEqual(Speaker.objects.count(), 1)

    def test_should_not_allow_to_create_new_speaker_via_api(self):
        speaker_data = {"name": "Speaker1", "description": "Description1", "image": "uploads/speakers/1.jpg", "priority": 1}

        response = self.client.post("/api/speakers/", speaker_data)

        self.assertEqual(response.status_code, 403)
