from django.conf import settings
from django.db import models


class Entry(models.Model):
    """An Entry is an entity that can be voted on in a poll."""
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.name


class Poll(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_accepting_entries = models.BooleanField(
        default=False,
        help_text='Are users able to submit entries?',
    )
    is_accepting_votes = models.BooleanField(
        default=False,
        help_text='Are users able to vote on entries in this poll?',
    )
    entries = models.ManyToManyField(Entry, related_name='polls', blank=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'poll', 'entry')

    def __str__(self):
        return '{} on {}'.format(self.user, self.poll)
