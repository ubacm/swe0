from django.urls import path

from swe0.events import views


app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('check-in/', views.CheckInView.as_view(), name='check-in'),
]
