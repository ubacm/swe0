from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, ListView

from swe0.polls.models import Entry, Poll, Vote


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ('name', 'description')


class EntryDetailView(DetailView):
    model = Entry

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            polls=self.object.polls.filter(is_accepting_votes=True),
        )


class PollDetailView(DetailView):
    model = Poll


class PollListView(ListView):
    model = Poll
    ordering = ['-id']


class VoteView(LoginRequiredMixin, FormView):
    template_name = 'polls/vote_form.html'
    form_class = forms.Form

    def dispatch(self, request, *args, **kwargs):
        self.poll = get_object_or_404(Poll, pk=kwargs.get('poll_pk'))
        self.entry = get_object_or_404(
            Entry,
            pk=kwargs.get('entry_pk'),
            polls=self.poll,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            poll=self.poll,
            entry=self.entry,
        )

    def form_valid(self, form):
        vote, created = Vote.objects.get_or_create(
            user=self.request.user,
            poll=self.poll,
            entry=self.entry,
        )
        if created:
            messages.success(
                self.request,
                'You have voted for {!r} in {!r}.'.format(
                    self.entry,
                    self.poll,
                ),
            )
        else:
            messages.info(
                self.request,
                'You already voted for {!r} in {!r}.'.format(
                    self.entry,
                    self.poll,
                ),
            )
        return super().form_valid(form)

    def get_success_url(self):
        return self.entry.get_absolute_url()
