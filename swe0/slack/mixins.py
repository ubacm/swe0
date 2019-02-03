import hashlib
import hmac
import time

from django.conf import settings
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class VerifySlackMixin:
    """Disable CSRF checks and verify that the request was signed by Slack."""
    # See https://api.slack.com/docs/verifying-requests-from-slack

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        _verify_slack_signature(request)
        return super().dispatch(request, *args, **kwargs)


def _validate_timestamp(request):
    """Validate the time range of the request (e.g. to prevent replay attacks)."""
    timestamp = int(request.META.get('HTTP_X_SLACK_REQUEST_TIMESTAMP', 0))
    if abs(time.time() - timestamp) > 60 * 5:
        raise SuspiciousOperation
    return timestamp


def _verify_slack_signature(request):
    timestamp = _validate_timestamp(request)

    signing_key = settings.SWE0_SLACK_SIGNING_SECRET.encode()
    signed_message = 'v0:{}:'.format(timestamp).encode() + request.body
    expected_signature = 'v0={}'.format(
        hmac.new(signing_key, signed_message, hashlib.sha256).hexdigest(),
    )

    actual_signature = request.META.get('HTTP_X_SLACK_SIGNATURE', '')

    if not hmac.compare_digest(expected_signature, actual_signature):
        raise PermissionDenied
