from django.contrib.auth.models import User
from .models import Profile, DonationPlace, Donation
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


class DeleteUserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class DonationPlaceForm(forms.ModelForm):
    class Meta:
        model = DonationPlace
        exclude = ('contributor', 'published',)


class InviteForm(forms.Form):
    email = forms.EmailField(required=True)


class AddDonationForm(forms.ModelForm):
    donationdate = forms.DateField(label='Donation date', initial=datetime.now(),
                                widget=forms.DateInput(attrs={
                                    'type': 'date'
                                }))

    class Meta:
        model = Donation
        exclude = ('created_at', 'updated_at', 'user')

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("donationdate")

        def clean_recipients(self):
            data = self.cleaned_data['recipients']
            if "fred@example.com" not in data:
                raise forms.ValidationError("You have forgotten about Fred!")

            # Always return a value to use as the new cleaned data, even if
            # this method didn't change it.
            return data
