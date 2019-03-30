from django.test import TestCase


class CoreTests(TestCase):

    def test_admin_login_redirect(self):
        response = self.client.get('/admin/login/')
        self.assertRedirects(response, '/accounts/login/')
