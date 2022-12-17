from datetime import datetime

from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from speeches.models import Speaker, Topic


class TopicViewTestCase(APITestCase):
    list_url = reverse_lazy("speeches:topic-list")

    @classmethod
    def setUpTestData(cls):
        cls.speakers_data = [
            {"name": "Speaker1", "description": "Description1", "image": "uploads/speakers/1.jpg", "priority": 1},
            {"name": "Speaker2", "description": "Description2", "image": "uploads/speakers/2.jpg", "priority": 1},
        ]

        Speaker.objects.bulk_create([Speaker(**speaker) for speaker in cls.speakers_data])

    def tearDown(self) -> None:
        Topic.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        Speaker.objects.all().delete()

    def _create_topic_with_speakers(self, data: list[dict]):
        speakers = [x["speakers"] for x in data]
        topics = [{k: v for k, v in topic.items() if k != "speakers"} for topic in data]

        Topic.objects.bulk_create([Topic(**topic) for topic in topics])

        for topic, speaker in zip(Topic.objects.order_by("-id")[: len(data) : -1], speakers):
            topic.speakers.set(speaker)
            topic.save()

    def test_should_return_list_of_topics(self):
        first_speaker = Speaker.objects.first()
        current_date = datetime.now()

        topics_data = [
            {
                "name": "Topic1",
                "description": "Description1",
                "start_date": current_date,
                "finish_date": current_date,
                "speakers": [first_speaker],
            },
            {
                "name": "Topic2",
                "description": "Description2",
                "start_date": current_date,
                "finish_date": current_date,
                "speakers": [first_speaker],
            },
        ]

        self._create_topic_with_speakers(topics_data)

        response = self.client.get(self.list_url)

        for response_topic, expected_topic in zip(response.data, topics_data):
            self.assertEqual(response_topic["name"], expected_topic["name"])
            self.assertEqual(len(response_topic["speakers"]), 1)
            self.assertEqual(response_topic["speakers"][0]["name"], first_speaker.name)

    def test_should_return_list_in_a_valid_order(self):
        first_speaker = Speaker.objects.first()
        current_date = datetime.now()

        topics_data = [
            {
                "name": "Topic1",
                "description": "Description1",
                "start_date": current_date,
                "finish_date": current_date,
                "speakers": [first_speaker],
                "priority": 1,
            },
            {
                "name": "Topic2",
                "description": "Description2",
                "start_date": current_date,
                "finish_date": current_date,
                "speakers": [first_speaker],
                "priority": 2,
            },
        ]

        self._create_topic_with_speakers(topics_data)

        response = self.client.get(self.list_url)

        self.assertEqual(response.data[0]["name"], topics_data[1]["name"])
        self.assertEqual(response.data[1]["name"], topics_data[0]["name"])

    def test_should_not_show_topic_with_priority_0(self):
        topic = Topic.objects.create(
            name="Topic1",
            description="Description1",
            start_date=datetime.now(),
            finish_date=datetime.now(),
            priority=0,
        )
        topic.speakers.add(Speaker.objects.first())
        topic.save()

        response = self.client.get(self.list_url)

        self.assertEqual(response.data, [])
        self.assertEqual(Topic.objects.count(), 1)

    def test_should_not_allow_to_create_new_topic_via_api(self):
        topic_data = {
                "name": "Topic1",
                "description": "Description1",
                "start_date": datetime.now(),
                "finish_date": datetime.now(),
                "speakers": [1],
            }

        response = self.client.post("/api/topics/", topic_data)

        self.assertEqual(response.status_code, 403)
