from django.conf import settings
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    amount = models.SmallIntegerField()
    comment = models.CharField(max_length=255)

    @classmethod
    def get_sum_for(cls, user):
        result = cls.objects.filter(user=user).aggregate(models.Sum('amount'))
        return result['amount__sum']
