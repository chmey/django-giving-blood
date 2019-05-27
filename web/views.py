from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm, InviteForm
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.template.loader import get_template
from django.template import Context
from .apps import WebConfig
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views


def index(request):
    context = {}
    return render(request, 'web/index.html', context)


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
def profile(request):
    return render(request, 'web/profile.html', {'user': request.user})


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


@login_required
def delete_user(request):
    try:
        u = request.user
        u.delete()
        messages.success(request, 'User deleted.')
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')

    logout(request)
    return render(request, 'web/index.html')


def faq(request):
	return render(request, 'web/faq.html')
