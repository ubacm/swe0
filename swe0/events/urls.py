from django.urls import path

from swe0.events import views


app_name = 'events'

urlpatterns = [
    path('check-in/', views.CheckInView.as_view(), name='check-in'),
]
