from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from swe0.polls import models


@admin.register(models.Entry)
class EntryAdmin(GuardedModelAdmin):
    pass


class PollEntriesInline(admin.TabularInline):
    model = models.Poll.entries.through


@admin.register(models.Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = (PollEntriesInline,)
    exclude = ('entries',)
    list_display = ('name', 'event', 'is_accepting_entries', 'is_accepting_votes')


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'user', 'entry')
    list_filter = ('poll', 'entry')
