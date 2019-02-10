from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from swe0.events.forms import CheckInForm
from swe0.events.models import CheckIn, Event


class CheckInView(LoginRequiredMixin, FormView):
    template_name = 'events/check_in.html'
    form_class = CheckInForm
    success_url = reverse_lazy('events:check-in')

    def form_valid(self, form):
        # Assuming the needed Event exists since we already performed validation.
        result = CheckIn.using_code(
            form.cleaned_data['check_in_code'],
            self.request.user,
        )
        messages.success(self.request, result.message)
        return super().form_valid(form)


class EventListView(ListView):
    model = Event
