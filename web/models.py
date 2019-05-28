from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils import timezone
from datetime import datetime, timedelta


class Profile(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_DIVERSE = 2
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_DIVERSE, 'Diverse')]

    BLOODTYPE_0n = 0
    BLOODTYPE_0p = 1
    BLOODTYPE_An = 2
    BLOODTYPE_Ap = 3
    BLOODTYPE_Bn = 4
    BLOODTYPE_Bp = 5
    BLOODTYPE_ABn = 6
    BLOODTYPE_ABp = 7
    BLOODTYPE_CHOICES = [(BLOODTYPE_0n, '0-'), (BLOODTYPE_0p, '0+'), (BLOODTYPE_An, 'A-'), (BLOODTYPE_Ap, 'A+'),
                         (BLOODTYPE_Bn, 'B-'), (BLOODTYPE_Bp, 'B+'), (BLOODTYPE_ABn, 'AB-'), (BLOODTYPE_ABp, 'AB+')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.SmallIntegerField(null=True, blank=True, choices=GENDER_CHOICES)
    bloodtype = models.SmallIntegerField(null=True, blank=True, choices=BLOODTYPE_CHOICES)
    birthdate = models.DateField(null=True, blank=True)
    receive_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_last_donation_date(self):
        return Donation.objects.latest('donationdate').donationdate

    def get_next_donation_date(self):
        return self.get_last_donation_date() + timedelta(days=56)

    def get_all_donations(self):
        return Donation.objects.filter(user=self.user)

    def date_in_allowed_interval(self, check_date):
        user_donations = self.get_all_donations()
        return not user_donations.filter(donationdate__range=
                                                [
                                                    check_date - timedelta(days=56),
                                                    check_date + timedelta(days=56)
                                                ])


class DonationPlace(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=5, blank=True)
    address_supplement = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=32)
    city = models.CharField(max_length=100)
    country = CountryField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name) + " in street " + str(self.street) + ", city: " + str(self.name) + ". Country: " + str(self.get_country_display())


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = False)
    donationdate = models.DateTimeField(default=timezone.now, blank = False)
    place = models.ForeignKey(DonationPlace, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
