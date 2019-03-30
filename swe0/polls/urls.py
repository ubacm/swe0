from django.urls import path

from swe0.polls import views


app_name = 'polls'

urlpatterns = [
    path('', views.PollList.as_view(), name='list'),
    path('<int:pk>/', views.PollDetail.as_view(), name='detail'),
    path('entries/<int:pk>/', views.EntryDetail.as_view(), name='entry-detail'),
]
