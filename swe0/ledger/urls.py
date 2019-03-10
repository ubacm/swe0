from django.urls import path

from swe0.ledger import views


app_name = 'ledger'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction-list'),
    path('users/<int:user_id>/', views.TransactionListView.as_view(), name='user-transaction-list'),
]
