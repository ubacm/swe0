from django.urls import path

from swe0.accounts import views


app_name = 'accounts'

urlpatterns = [
    path('logout/', views.LogOutView.as_view(), name='log-out'),
]
