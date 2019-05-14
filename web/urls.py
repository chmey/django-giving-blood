from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'web'
urlpatterns = [
        path('', views.index, name='index'),
        path('auth/login', auth_views.LoginView.as_view(template_name='web/login.html',redirect_authenticated_user=True), name='login'),
        path('auth/logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
        path('auth/signup', views.signup, name='signup'),
        path('profile', views.profile, name='profile'),
        path('auth/reset/init', auth_views.PasswordResetView.as_view(), name="assword_reset"),
        path('auth/reset/done', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
        path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('auth/reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]
