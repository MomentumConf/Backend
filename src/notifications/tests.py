from django.urls import reverse_lazy

from rest_framework.test import APITestCase

from notifications.models import Subscription


class SubscriptionViewTestCase(APITestCase):
    create_url = reverse_lazy("notifications:subscription-list")

    def tearDown(self) -> None:
        Subscription.objects.all().delete()

    def test_should_throw_error_when_trying_get_method(self):
        response = self.client.get("/api/subscriptions/")

        self.assertEqual(response.status_code, 405)

    def test_should_create_a_new_subscription(self):
        data = {"details": '{"keys": {"auth":"test"}}'}

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_should_not_create_a_new_subscription_when_using_the_same_auth(self):
        data = {"details": '{"keys": {"auth":"test"}}'}

        response = self.client.post(self.create_url, data)
        response_reuse = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_reuse.status_code, 201)
        self.assertEqual(Subscription.objects.count(), 1)
