from django.contrib import admin

from swe0.events import models


@admin.register(models.CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('time', 'event', 'user')
    list_filter = ('event',)


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'location', 'check_in_code', 'check_in_enabled')
