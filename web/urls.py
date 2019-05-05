from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'web'
urlpatterns = [
        path('', views.index, name='index'),
        path('login', auth_views.LoginView.as_view(template_name='web/login.html'), name='login'),
        path('logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
        path('signup', views.signup, name='signup'),
        path('profile', views.profile, name='profile')
    ]
