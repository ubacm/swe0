from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from swe0.events import forms


class CheckInView(LoginRequiredMixin, FormView):
    template_name = 'events/check_in.html'
    form_class = forms.CheckInForm
    success_url = reverse_lazy('events:check-in')

    def form_valid(self, form):
        # Assuming the needed Event exists since we already performed validation.
        checked_in = form.check_in(self.request.user)
        if checked_in:
            messages.success(self.request, 'You have successfully checked in.')
        else:
            messages.success(self.request, 'You had already checked in.')
        return super().form_valid(form)
