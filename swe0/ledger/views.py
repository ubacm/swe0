from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from swe0.ledger.models import Transaction


User = get_user_model()


class TransactionListView(PermissionRequiredMixin, ListView):
    permission_required = 'ledger.view_transaction'
    model = Transaction
    ordering = ['-time']

    def get_queryset(self):
        queryset = super().get_queryset()

        user_id = self.kwargs.get('user_id')
        if user_id is not None:
            user = get_object_or_404(User, id=user_id)
            queryset = queryset.filter(user=user)

        return queryset
