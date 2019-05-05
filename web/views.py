from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def index(request):
    context = {}
    return render(request, 'web/index.html', context)
def login(request):
    return render(request, 'web/login.html', {})
def logout(request):
    return HttpResponse()
def signup(request):
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
    return render(request, 'web/signup.html', {'form': form})

def profile(request):
    return render(request, 'web/profile.html', {'user': request.user})
