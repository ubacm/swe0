from django.views.generic import DetailView, ListView

from swe0.polls.models import Poll


class PollDetail(DetailView):
    model = Poll


class PollList(ListView):
    model = Poll
    ordering = ['-id']
