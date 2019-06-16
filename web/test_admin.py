from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import DonationPlace
from django.urls import reverse
from datetime import datetime

class AdminTest(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        self._u = User.objects.create_superuser('testcaseadmin', email='lazy@lazy.com', password='testcasepw')
        self._place = DonationPlace.objects.create(contributor=self._u, name='Test', street='Test', postal_code='123', city='Test', country='DE')

    def test_add_news_get(self):
        self.client.login(username='testcaseadmin', password='testcasepw')
        resp = self.client.get(reverse('admin:add-news'))
        self.assertTemplateUsed(resp, 'admin/add_news.html')

    def test_add_news_post(self):
        self.client.login(username='testcaseadmin', password='testcasepw')
        resp = self.client.post(reverse('admin:add-news'), {'title': 'Test', 'body': 'Test', 'date': datetime.now().date()})
        print(resp.context)
        self.assertRedirects(resp, reverse('news'))

    def test_add_news_post_fail(self):
        self.client.login(username='testcaseadmin', password='testcasepw')
        resp = self.client.post(reverse('admin:add-news'), {'title': 'Test', 'body': 'Test'})
        self.assertFormError(resp, 'form', 'date', 'This field is required.')

    def test_eview_place_get_id_none(self):
        self.client.login(username='testcaseadmin', password='testcasepw')
        resp = self.client.get(reverse('admin:review-place-index'))
        self.assertTemplateUsed(resp, 'admin/review_place_index.html')

    def test_review_place_get_id_1(self):
        self.client.login(username='testcaseadmin', password='testcasepw')
        resp = self.client.get(reverse('admin:review-place', args=[1]))
        self.assertTemplateUsed(resp, 'admin/review_place.html')

    def test_review_place_post_id_1(self):
        self.client.login(username='testcaseadmin', password='testcasepw', follow=True)
        self.client.post(reverse('admin:review-place', args=[1]), {'approve':'true'})
        self.assertTrue(DonationPlace.objects.get(id=1).published)

    def test_import_donation_places_get(self):
        self.client.login(username='testcaseadmin', password='testcasepw', follow=True)
        resp = self.client.get(reverse('admin:upload-donation-places'))
        self.assertTemplateUsed(resp, 'admin/upload_donations_places.html')
