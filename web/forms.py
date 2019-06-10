from django.contrib.auth.models import User
from .models import Profile, DonationPlace, Donation
from django import forms
from datetime import datetime
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    birthdate = forms.DateField(label='Birth date', initial=datetime.now(),
                                widget=forms.DateInput(attrs={
                                    'type': 'date'
                                }))

    class Meta:
        model = Profile
        fields = ('gender', 'birthdate', 'bloodtype', 'receive_notifications')


class DeleteUserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class DonationPlaceForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    house = forms.CharField(label='Street Number', max_length=5, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    address_supplement = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(label='Postal/ZIP code', max_length=32, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = CountryField().formfield(widget=CountrySelectWidget(attrs={'class': 'form-control'}))


    class Meta:
        model = DonationPlace
        exclude = ('contributor', 'published',)


class InviteForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))


class AddDonationForm(forms.ModelForm):
    donationdate = forms.DateField(label='Date of Blood Donation', initial=datetime.now(),
                                widget=forms.DateInput(attrs={
                                    'type': 'date', 'class': 'form-control'
                                }))
    place = forms.ModelChoiceField(queryset=DonationPlace.objects.all(), label='Facility (optional)',widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Donation
        exclude = ('created_at', 'updated_at', 'user')
