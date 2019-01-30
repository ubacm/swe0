import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from swe0.profiles.models import Profile


class ResumeUploadView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'profiles/resume_upload.html'
    model = Profile
    fields = ('resume',)
    success_message = 'Your resume was successfully updated.'
    # TODO: use a more appropriate view for success_url when available
    success_url = reverse_lazy('profiles:resume-upload')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        obj, created = queryset.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        previous_resume = form['resume'].initial
        response = super().form_valid(form)
        if previous_resume:
            os.remove(previous_resume.path)
        return response
