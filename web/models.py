from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_DIVERSE = 2
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_DIVERSE, 'Diverse')]

    BLOODTYPE_0 = 0
    BLOODTYPE_A = 1
    BLOODTYPE_B = 2
    BLOODTYPE_AB = 3
    BLOODTYPE_CHOICES = [(BLOODTYPE_0, '0'), (BLOODTYPE_A, 'A'), (BLOODTYPE_B, 'B'), (BLOODTYPE_AB, 'AB')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.SmallIntegerField(null=True, blank=True, choices=GENDER_CHOICES)
    bloodtype = models.SmallIntegerField(null=True, blank=True, choices=BLOODTYPE_CHOICES)
    birthdate = models.DateField(null=True, blank=True)
    receive_notifications = models.BooleanField(default=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
