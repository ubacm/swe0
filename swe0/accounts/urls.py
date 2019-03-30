from django.urls import path

from swe0.accounts import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.LogInView.as_view(), name='log-in'),
    path('login/local/', views.LocalLogInView.as_view(), name='local-log-in'),
    path('logout/', views.LogOutView.as_view(), name='log-out'),
]
