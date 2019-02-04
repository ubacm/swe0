from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
import requests

from swe0.accounts.utils import email_address_is_whitelisted
from swe0.events.models import CheckIn, Event
from swe0.slack.mixins import VerifySlackMixin


User = get_user_model()


class CheckInView(VerifySlackMixin, View):
    def post(self, *_args, **_kwargs):
        check_in_code = self.request.POST['text']
        user = self.get_user()

        result = CheckIn.using_code(check_in_code, user)
        return HttpResponse(result.message)

    def get_user(self):
        slack_user_id = self.request.POST['user_id']
        slack_profile = self._get_user_slack_profile(slack_user_id)
        if not slack_profile:
            raise PermissionDenied

        email = slack_profile['email']
        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            if not email_address_is_whitelisted(email):
                raise PermissionDenied
            user = User.objects.create_user(email=email, name=slack_profile['real_name'])

        return user

    @staticmethod
    def _get_user_slack_profile(user_id):
        response = requests.post(
            'https://slack.com/api/users.profile.get',
            data={'user': user_id},
            headers={
                'Authorization': 'Bearer {}'.format(settings.SWE0_SLACK_API_TOKEN),
            },
        )
        data = response.json()
        return data.get('profile')
