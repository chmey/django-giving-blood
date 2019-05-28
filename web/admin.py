from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.urls import path
from .models import DonationPlace, Donation, Profile
from news.models import Article
from . import admin_views


class BloodAdminSite(AdminSite):
    site_header = 'Administration'

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('review_place/<id>', admin_views.review_place),
        ]
        return urls + admin_urls


admin_site = BloodAdminSite(name='bloodadmin')
admin_site.register([Donation, DonationPlace, Profile, User, Article])
