from django.apps import apps
from django.test import TestCase
from .apps import WebConfig


class WebConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(WebConfig.name, 'web')
        self.assertEqual(apps.get_app_config('web').name, 'web')
