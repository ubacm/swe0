# Generated by Django 2.1.7 on 2019-04-27 19:51

import django.core.validators
from django.db import migrations, models
import swe0.polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='image',
            field=models.ImageField(blank=True, upload_to=swe0.polls.models._generate_picture_filename, validators=[django.core.validators.FileExtensionValidator(['gif', 'jpeg', 'jpg', 'png', 'svg'])]),
        ),
        migrations.AddField(
            model_name='entry',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
