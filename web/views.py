from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate

def index(request):
    context = {}
    return render(request, 'web/index.html', context)
def login(request):
    return render(request, 'web/login.html', {})
def logout(request):
    return HttpResponse()
def register(request):
    return HttpResponse()
