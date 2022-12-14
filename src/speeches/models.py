from django.db import models


class Speaker(models.Model):
    class Meta:
        ordering = ["-priority"]

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="uploads/speakers/")
    priority = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class Topic(models.Model):
    class Meta:
        ordering = ["start_date", "-priority"]

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    priority = models.PositiveSmallIntegerField(default=1)
    speakers = models.ManyToManyField(Speaker)

    def __str__(self) -> str:
        return self.name
