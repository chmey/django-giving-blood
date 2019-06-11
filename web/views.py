from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm, InviteForm, DonationPlaceForm, AddDonationForm, DeleteUserForm
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.template.loader import get_template
from .apps import WebConfig
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Donation


def index(request):
    context = {}
    return render(request, 'web/index.html', context)


# AUTH VIEWS
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})


@login_required
def delete_user(request):
    if request.method == 'POST':
        try:
            u = request.user
            confirmation_form = DeleteUserForm(request.POST)
            if confirmation_form.is_valid():
                if u.check_password(confirmation_form.cleaned_data.get('password')):
                    u.delete()
                    messages.success(request, 'User deleted.')
                    logout(request)
                    return render(request, 'web/index.html')
                else:
                    messages.error(request, 'The password is wrong.')
            else:
                messages.error(request, 'Invalid input.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
    else:
        confirmation_form = DeleteUserForm()
    return render(request, 'web/delete_user.html', {
            'confirmation_form': confirmation_form
        })

# PROFILE VIEWS
@login_required
def profile(request):
    donation_form = AddDonationForm()
    return render(request, 'web/profile.html', {'donation_form': donation_form,'user': request.user, 'donations': request.user.profile.get_all_donations().all()})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'web/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# BLOOD DONATION VIEWS
@login_required
def add_donation(request):
    if request.method == 'POST':
        donation_form = AddDonationForm(request.POST)
        donation_form.instance.user = request.user
        if donation_form.is_valid():
            donation_form.save()
            messages.success(request, 'Donation added.')
            if not request.user.profile.date_in_allowed_interval(donation_form.instance.donationdate):
                messages.warning(request, "Be careful: The donation you added was too soon after your last blood donation. It is advised to wait 56 days between donations.")
            return redirect('profile')
        else:
            messages.error(request, 'Donation adding failed. Please correct the errors.')
    else:
        donation_form = AddDonationForm()
    return render(request, 'web/add_donation.html', {
        'donation_form': donation_form
    })


@login_required
def edit_donation(request, donation_id):
    instance = get_object_or_404(Donation, id=donation_id)
    form = AddDonationForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Donation edited.')
        if not request.user.profile.date_in_allowed_interval(form.instance.donationdate):
            messages.warning(request, "Be careful: The donation you added was too soon after your last blood donation. It is advised to wait 56 days between donations.")
        return redirect('profile')
    return render(request, 'web/add_donation.html', {
        'donation_form': form
    })


@login_required
def drop_donation(request, donation_id):
    instance = get_object_or_404(Donation, id=donation_id)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, 'Donation dropped.')
        return render(request, 'web/profile.html', {'user': request.user})
    return render(request, 'web/drop_donation.html')


@login_required
def invite(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            subject = get_template('email/invite_subject.txt').render().strip()
            con = {'user': request.user.email, 'url': request.build_absolute_uri(reverse('signup'))}
            plain = get_template('email/invite.txt').render(con)
            html_mail = get_template('email/invite.html').render(con)
            msg = EmailMultiAlternatives(subject=subject, body=plain, from_email=WebConfig.from_email_invite, to=[form.cleaned_data['email']])
            msg.attach_alternative(html_mail, 'text/html')
            msg.send()
            messages.success(request, 'Your invitation was sent')
        else:
            messages.error(request, 'Invitation failed. Please correct the errors.')
    else:
        form = InviteForm()
    return render(request, 'web/invite.html', {'form': form})


def faq(request):
    return render(request, 'web/faq.html')


def news(request):
    return render(request, 'news/index.html')


@login_required
def add_donation_place(request):
    if request.method == 'POST':
        form = DonationPlaceForm(request.POST)
        form.instance.contributor = request.user
        form.instance.published = False
        if form.is_valid():
            new_place = form.save()
            url = request.build_absolute_uri(reverse('admin:review-place', args=(new_place.pk, )))
            subject = get_template('email/addplace_subject.txt').render().strip()
            plain = get_template('email/addplace.txt').render({'url': url})
            html_mail = get_template('email/addplace.html').render({'url': url})
            msg = EmailMultiAlternatives(subject=subject, body=plain, from_email=WebConfig.from_email_admin, to=[WebConfig.from_email_admin])
            msg.attach_alternative(html_mail, 'text/html')
            msg.send()
            messages.success(request, 'Donation facility was added and has to be reviewed by staff.')
        else:
            messages.error(request, 'The form contains errors. Please correct them.')
    else:
        form = DonationPlaceForm()
    return render(request, 'web/add_donation_place.html', {'form': form})
