from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils import timezone


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


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    place = models.ForeignKey(DonationPlace, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
