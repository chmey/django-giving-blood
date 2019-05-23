from django.contrib.auth.models import User
from .models import Profile, DonationPlace
from django import forms
from datetime import datetime


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


class DonationPlaceForm(forms.ModelForm):
    class Meta:
        model = DonationPlace
        exclude = ('contributor', 'published',)


class InviteForm(forms.Form):
    email = forms.EmailField(required=True)
