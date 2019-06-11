from django.test import TestCase
from datetime import datetime
from .forms import AddDonationForm


class DonationTestCase(TestCase):

    def test_add_donation(self):
        form_data = {'something': 'something'}
        form = MyForm(data=form_data)
        self.assertTrue(form.is_valid())
 
    
    def test_search_donation(self):
        pass
    
    def test_edit_donation(self):
        pass
    
    def test_count_donations(self):
        pass
    
    def test_drop_donations(self):
        pass

    
