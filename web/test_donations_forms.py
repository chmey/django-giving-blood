from django.test import TestCase
from datetime import datetime
from .models import Donation
from django.shortcuts import get_object_or_404

class DonationTestCase(TestCase):

    def test_donations(self):
        
        self.client = Client()
        
        #donation failed
        form_data = {'place': 'Place1 , Via 1 , 24048 Treviolo HU'}
        response = self.client.post('/add/', form_data)
        self.assertFormError(response, 'form', 'donationdate', 'This field is required.')
        
        #donation done
        form_data = {'donationdate': datetime(2019, 6, 11), 'place': 'Place1 , Via 1 , 24048 Treviolo HU'}
        response = self.client.post("/add/", form_data)
        self.assertTrue(response, 200)
        form_data = {'donationdate': datetime(2019, 9, 23), 'place': 'Place2 , Via 2 , 46363 Krakow PL'}
        response = self.client.post("/add/", form_data)
        self.assertTrue(response, 200)      
        form_data = {'donationdate': datetime(2020, 7, 15), 'place': 'Place3 , Via 3 , 52525 Dalmine IT'}
        response = self.client.post("/add/", form_data)
        self.assertTrue(response, 200)
        
        #donation found
        instance = get_object_or_404(Donation, id=2)
        self.assertTrue(instance.donationdate, datetime(2020, 7, 15))
        self.assertTrue(instance.place, 'Place3 , Via 3 , 52525 Dalmine IT')
        
        #number of donations
        
        
        #edit a donation
        response = self.client.post("/edit/2", {'donationdate': datetime(2020, 6, 11), 'place': 'Place1 , Via 1 , 24048 Treviolo HU'})
        self.assertTrue(response, 200)
        instance = get_object_or_404(Donation, id=1)
        self.assertTrue(instance.donationdate, datetime(2020, 6, 11))
        self.assertTrue(instance.place, 'Place1 , Via 1 , 24048 Treviolo HU')
        
        #drop a donation
        response = self.client.post("/drop/0")
        self.assertTrue(response, 200)
