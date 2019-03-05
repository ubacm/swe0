from django.urls import path

from swe0.profiles import views


app_name = 'profiles'

urlpatterns = [
    path('<int:user_id>/', views.ProfileDetailView.as_view(), name='view'),
    path('upload-resume/', views.ResumeUploadView.as_view(), name='resume-upload'),
]
