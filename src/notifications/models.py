import uuid

from django.db import models


class Subscription(models.Model):
    auth = models.CharField(max_length=255, unique=True)
    details = models.JSONField()


class Notification(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    send_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
