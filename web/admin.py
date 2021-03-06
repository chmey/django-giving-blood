from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.urls import path
from .models import DonationPlace, Donation, Profile, Article
from . import admin_views


class BloodAdminSite(AdminSite):
    site_header = 'Administration'

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('review_place/<id>', admin_views.review_place, name='review-place'),
            path('review_place', admin_views.review_place, name='review-place-index'),
            path('import_donation_places', admin_views.import_donation_places, name='upload-donation-places'),
            path('add_news', admin_views.add_news, name='add-news'),
        ]
        return urls + admin_urls


admin_site = BloodAdminSite(name='bloodadmin')
admin_site.register([Donation, DonationPlace, Profile, User, Article])
