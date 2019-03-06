import os

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView

from swe0.profiles.models import Profile


User = get_user_model()


class ProfileFromUserIdMixin:
    """Provide a user's profile using user_id matched in the URL."""

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)

        obj, created = queryset.get_or_create(user=user)
        return obj


class ProfileDetailView(ProfileFromUserIdMixin, DetailView):
    model = Profile


# TODO: delete old pictures and resumes
class ProfileUpdateView(UserPassesTestMixin, ProfileFromUserIdMixin, UpdateView):
    model = Profile
    fields = ('biography', 'graduation_year', 'personal_website', 'picture', 'resume')

    def test_func(self):
        """Allow users to only edit their own profiles."""
        profile = self.get_object()
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse('profiles:view', kwargs={'user_id': self.object.user.id})


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
