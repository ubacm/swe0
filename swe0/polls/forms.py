from django import forms

from swe0.polls.models import Entry, Poll


class EntryForm(forms.ModelForm):
    polls = forms.ModelMultipleChoiceField(
        Poll.objects.filter(is_accepting_entries=True),
    )

    class Meta:
        model = Entry
        fields = ('name', 'description')

    def save(self, commit=True):
        entry = super().save(commit)
        for poll in self.cleaned_data['polls']:
            poll.entries.add(entry)
        return entry
