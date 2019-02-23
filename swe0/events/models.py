from collections import namedtuple
import itertools

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


CheckInResult = namedtuple('CheckInResult', ['is_checked_in', 'message'])


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    check_in_enabled = models.BooleanField(default=False)
    check_in_code = models.CharField(
        max_length=25,
        unique=True,
        blank=True,
        help_text='If empty, a code will automatically be generated.',
    )
    check_in_rewards = models.IntegerField(default=1)

    # Attempt to eliminate potentially confusing characters.
    CHECK_IN_CODE_ALLOWED_CHARS = 'ABDEFGHJMNPQRTYabdefghjmnpqrty23456789'

    class Meta:
        ordering = ('-start_time', '-end_time', 'title')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.check_in_code:
            self.check_in_code = self._generate_check_in_code()
        return super().save(*args, **kwargs)

    @classmethod
    def _generate_check_in_code(cls):
        """Generate a unique check in code for an Event."""
        for _ in itertools.count():
            code = get_random_string(
                length=5,
                allowed_chars=cls.CHECK_IN_CODE_ALLOWED_CHARS,
            )
            if not cls.objects.filter(check_in_code=code).exists():
                return code


class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = 'check-in'

    def __str__(self):
        return '{} at {}'.format(self.user, self.event)

    @classmethod
    def using_code(cls, check_in_code, user) -> CheckInResult:
        try:
            event = Event.objects.get(check_in_code=check_in_code)
        except Event.DoesNotExist:
            return CheckInResult(False, 'The check-in code is invalid.')

        if not event.check_in_enabled:
            return CheckInResult(False, 'The event is not currently accepting check-ins.')

        obj, created = cls.objects.get_or_create(event=event, user=user)
        if created:
            return CheckInResult(True, 'You have successfully checked in.')
        return CheckInResult(True, 'You had already checked in.')
