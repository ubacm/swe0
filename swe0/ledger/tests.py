from django.contrib.auth import get_user_model
from django.test import TestCase

from swe0.ledger.models import Transaction


User = get_user_model()


class TransactionTest(TestCase):

    def test_sum(self):
        user = User.objects.create(email='test@example.com')
        irrelevant_user = User.objects.create(email='noise@example.com')

        irrelevant_transaction = Transaction.objects.create(
            user=irrelevant_user,
            amount=7,
            comment='Irrelevant',
        )
        increase_transaction = Transaction.objects.create(
            user=user,
            amount=3,
            comment='Increase',
        )
        decrease_transaction = Transaction.objects.create(
            user=user,
            amount=-1,
            comment='Decrease',
        )

        actual_sum = Transaction.get_sum_for(user)
        self.assertEqual(actual_sum, 2)
