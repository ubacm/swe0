import csv
import io
import os
import zipfile

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import FileResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, View

from swe0.profiles.models import Profile


class ResumeExportView(PermissionRequiredMixin, View):
    permission_required = 'profiles.view_profile'

    @staticmethod
    def get_export_list():
        for profile in Profile.objects.all():
            if profile.resume:
                yield profile.resume.path, profile.user

    def get_archive(self):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as archive:
            csv_buffer = io.StringIO()
            csv_writer = csv.DictWriter(csv_buffer, fieldnames=['name', 'email', 'filename'])
            csv_writer.writeheader()
            for filename, user in self.get_export_list():
                data = {
                    'name': user.name,
                    'email': user.email,
                }
                arcname = '{name}_{email}_resume.pdf'.format_map(data)
                archive.write(filename, arcname)
                csv_writer.writerow({**data, 'filename': arcname})
            archive.writestr('_resumes_index.csv', csv_buffer.getvalue())
        zip_buffer.seek(0)
        return zip_buffer

    def get(self, *args, **kwargs):
        filename = timezone.localtime().strftime('resumes_%Y-%m-%d-%H-%M.zip')
        return FileResponse(self.get_archive(), as_attachment=True, filename=filename)


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
