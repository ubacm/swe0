import itertools
import os
import uuid

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


def _generate_picture_filename(_instance, original_filename):
    extension = os.path.splitext(original_filename)[1].lower()
    for _ in itertools.count():
        filename = os.path.join(
            'profiles',
            'pictures',
            '{}{}'.format(uuid.uuid4().hex, extension),
        )
        if not Profile.objects.filter(picture=filename).exists():
            return filename


def _generate_resume_filename(*_args):
    for _ in itertools.count():
        filename = os.path.join(
            'profiles',
            'resumes',
            '{}.pdf'.format(uuid.uuid4().hex),
        )
        if not Profile.objects.filter(resume=filename).exists():
            return filename


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    biography = models.TextField(blank=True)
    graduation_year = models.PositiveSmallIntegerField(blank=True, null=True)
    personal_website = models.URLField(blank=True)
    picture = models.ImageField(
        upload_to=_generate_picture_filename,
        validators=[FileExtensionValidator(['gif', 'jpeg', 'jpg', 'png', 'svg'])],
        blank=True,
    )
    resume = models.FileField(
        upload_to=_generate_resume_filename,
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
    )

    def __str__(self):
        return 'Profile for {}'.format(self.user)
