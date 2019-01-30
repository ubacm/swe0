from django.contrib import admin

from swe0.events import models


admin.site.register(models.CheckIn)
admin.site.register(models.Event)
