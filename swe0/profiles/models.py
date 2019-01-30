import itertools
import os
import uuid

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


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
    resume = models.FileField(
        upload_to=_generate_resume_filename,
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
    )
