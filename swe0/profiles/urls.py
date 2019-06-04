from django.urls import path
from django.views.generic import RedirectView

from swe0.profiles import views


app_name = 'profiles'

urlpatterns = [
    path('resumes/export/', views.ResumeExportView.as_view(), name='export-resumes'),
    path('resumes/upload/', views.ResumeUploadView.as_view(), name='upload-resume'),
    path('upload-resume/', RedirectView.as_view(pattern_name='profiles:upload-resume'), name='resume-upload'),
]
