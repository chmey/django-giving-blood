from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import datetime


class ViewsTestCase(TestCase):
    def setUp(self):
        pass

    def test_index_template_anon(self):
        c = Client()
        resp = c.get('/')
        self.assertTemplateUsed(resp, 'web/index.html')

    def test_index_template_user(self):
        c = Client()
        u = User.objects.create_user('testcase')
        c.force_login(user=u)
        resp = c.get('/')
        self.assertTemplateUsed(resp, 'web/index.html')

    def test_signup_anon_template(self):
        c = Client()
        resp = c.get('/auth/signup')
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'auth/signup.html')

    def test_signup_user(self):
        c = Client()
        u = User.objects.create_user('testcase')
        c.force_login(user=u)
        resp = c.get('/auth/signup')
        # Assert logged in user has been redirected
        self.assertRedirects(resp, '/')

    def test_signup_anon_submit_empty(self):
        c = Client()
        resp = c.post('/auth/signup')
        self.assertTemplateUsed(resp, 'auth/signup.html')

    def test_signup_anon_submit_successful(self):
        c = Client()
        resp = c.post('/auth/signup', data={'username': 'testcase', 'password2': 'top_secret', 'password1':'top_secret'}, follow=True)
        self.assertTrue(resp.context['user'].is_authenticated)
        self.assertRedirects(resp, '/')

    def test_profile_anon(self):
        c = Client()
        resp = c.get('/profile')
        self.assertURLEqual(resp.url, '/auth/login?next=/profile')

    def test_profile_user(self):
        c = Client()
        u = User.objects.create_user('testcase')
        c.force_login(user=u)
        resp = c.get('/profile')
        self.assertTemplateUsed(resp, 'web/profile.html')
        self.assertEqual(resp.context['user'], u)

    def test_edit_profile_anon(self):
        c = Client()
        resp = c.get('/profile/edit')
        self.assertURLEqual(resp.url, '/auth/login?next=/profile/edit')

    def test_edit_profile_user_render(self):
        c = Client()
        u = User.objects.create_user('testcase')
        c.force_login(user=u)
        resp = c.get('/profile/edit')
        self.assertTemplateUsed(resp, 'web/edit_profile.html')
        self.assertEqual(resp.status_code, 200)

    def test_edit_profile_user_submit_empty(self):
        c = Client()
        u = User.objects.create_user('testcase')
        c.force_login(user=u)
        resp = c.post('/profile/edit')
        self.assertTrue(len(resp.context['messages']) > 0)
        self.assertTemplateUsed(resp, 'web/edit_profile.html')

    def test_edit_profile_user_submit_successful(self):
        c = Client()
        u = User.objects.create_user('testcase')
        c.force_login(user=u)
        resp = c.get('/profile/edit')
        data = {'first_name': 'Test', 'last_name': 'Case', 'email': 'test@localhost', 'birthdate': datetime.now().date().isoformat(), 'gender': 0, 'bloodtype': 0}
        resp = c.post('/profile/edit', data, follow=True)
        self.assertEquals(resp.context['user'].last_name, 'Case')
        self.assertRedirects(resp, '/profile')
