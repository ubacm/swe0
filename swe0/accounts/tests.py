from django.test import TestCase, override_settings

from swe0.accounts.utils import email_address_is_whitelisted


class UtilsTests(TestCase):
    @override_settings(SWE0_CREATE_USER_WHITELISTED_DOMAINS=[])
    def test_email_address_is_whitelisted_default(self):
        self.assertTrue(email_address_is_whitelisted('test@example.com'))

    @override_settings(SWE0_CREATE_USER_WHITELISTED_DOMAINS=['example.org'])
    def test_email_address_is_whitelisted_no(self):
        self.assertFalse(email_address_is_whitelisted('test@example.com'))

    @override_settings(SWE0_CREATE_USER_WHITELISTED_DOMAINS=['example.com', 'example.org'])
    def test_email_address_is_whitelisted_yes(self):
        self.assertTrue(email_address_is_whitelisted('test@example.com'))
