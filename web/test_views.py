from django.test import TestCase, Client
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
    def setUp(self):
        pass

    def test_render_signup_as_anon(self):
        c = Client()
        resp = c.get('/auth/signup')
        self.assertEquals(resp.status_code, 200)
        # TODO: Check correct template rendered

    def test_signup_as_logged_in(self):
        c = Client()
        u = User.objects.create_user('testcase')
        c.force_login(user=u)
        resp = c.get('/auth/signup')
        # Assert logged in user has been redirected
        self.assertRedirects(resp, '/')
