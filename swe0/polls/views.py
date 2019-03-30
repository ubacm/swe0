from django.views.generic import ListView

from swe0.polls.models import Poll


class PollList(ListView):
    model = Poll
    ordering = ['-id']
