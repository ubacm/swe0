from django.urls import path

from swe0.slack import views


app_name = 'slack'

urlpatterns = [
    path('check-in/', views.CheckInView.as_view(), name='check-in'),
]
