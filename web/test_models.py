from django.test import TestCase
from .models import Donation, Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class ProfileModelTest(TestCase):

    def testGetDateInAllowedIntervalFalse(self):
        u = User.objects.create()
        Donation.objects.create(user=u, donationdate=datetime.now())

        self.assertFalse(u.profile.date_in_allowed_interval(datetime.now()))

    def testGetDateInAllowedIntervalFalse2(self):
        u = User.objects.create()
        Donation.objects.create(user=u, donationdate=datetime.now())
        c_date = datetime.now() + timedelta(days=1)
        self.assertFalse(u.profile.date_in_allowed_interval(c_date))

    def testGetDateInAllowedIntervalTrue(self):
        u = User.objects.create()
        Donation.objects.create(user=u, donationdate=datetime.now())
        c_date = datetime.now() + timedelta(days=58)
        self.assertTrue(u.profile.date_in_allowed_interval(c_date))

    def testGetNextDonationDate(self):
        pass
