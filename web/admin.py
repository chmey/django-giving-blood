from django.contrib.admin import AdminSite
from .models import DonationPlace, Donation, Profile
from django.contrib.auth.models import User

class BloodAdminSite(AdminSite):
    site_header = 'Administration'

admin_site = BloodAdminSite(name='bloodadmin')
admin_site.register([Donation, DonationPlace, Profile])
