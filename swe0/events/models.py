import itertools

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    attendance_enabled = models.BooleanField(default=False)
    attendance_code = models.CharField(max_length=25, unique=True, blank=True)
    attendance_rewards = models.IntegerField(default=1)

    # Attempt to eliminate potentially confusing characters.
    ATTENDANCE_CODE_ALLOWED_CHARS = 'ABDEFGHJMNPQRTYabdefghjmnpqrty23456789'

    class Meta:
        ordering = ('start_time', 'end_time', 'title')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.attendance_code:
            self.attendance_code = self.generate_attendance_code()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_attendance_code(cls):
        """Generate a unique attendance code for an Event."""
        for _ in itertools.count():
            code = get_random_string(
                length=6,
                allowed_chars=cls.ATTENDANCE_CODE_ALLOWED_CHARS,
            )
            if not cls.objects.filter(attendance_code=code).exists():
                return code


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return '{} at {}'.format(self.user, self.event)
