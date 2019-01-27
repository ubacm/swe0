from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('start_time', 'end_time', 'title')

    def __str__(self):
        return self.title
