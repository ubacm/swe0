from django.views.generic import DetailView, ListView

from swe0.polls.models import Entry, Poll


class EntryDetail(DetailView):
    model = Entry


class PollDetail(DetailView):
    model = Poll


class PollList(ListView):
    model = Poll
    ordering = ['-id']
