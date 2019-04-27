from django.urls import path

from swe0.polls import views


app_name = 'polls'

urlpatterns = [
    path('', views.PollListView.as_view(), name='list'),
    path('<int:pk>/', views.PollDetailView.as_view(), name='detail'),
    path('<int:poll_pk>/vote/<int:entry_pk>/', views.VoteView.as_view(), name='vote'),
    path('entries/create/', views.EntryCreateView.as_view(), name='entry-create'),
    path('entries/<int:pk>/', views.EntryDetailView.as_view(), name='entry-detail'),
    path('entries/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry-update'),
]
