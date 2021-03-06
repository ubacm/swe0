from django import forms

from swe0.events.models import Event


class CheckInForm(forms.Form):
    check_in_code = forms.CharField()

    def clean_check_in_code(self):
        check_in_code = self.cleaned_data['check_in_code']
        try:
            event = Event.objects.get(check_in_code=check_in_code)
        except Event.DoesNotExist:
            raise forms.ValidationError(
                'The check in code {!r} is invalid.'.format(check_in_code)
            )
        if not event.check_in_enabled:
            raise forms.ValidationError(
                'The event is not currently accepting check-ins.'
            )
        return check_in_code
