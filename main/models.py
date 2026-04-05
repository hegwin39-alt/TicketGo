from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    image = models.URLField(max_length=500)
    description = models.TextField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title