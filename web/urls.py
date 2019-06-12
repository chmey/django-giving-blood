from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'web'
urlpatterns = [
        path('', views.index, name='index'),

        # AUTH URLs
        path('auth/login', auth_views.LoginView.as_view(template_name='auth/login.html',redirect_authenticated_user=True), name='login'),
        path('auth/logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
        path('auth/signup', views.signup, name='signup'),
        path('auth/change_password', auth_views.PasswordChangeView.as_view(template_name='auth/password_change.html'), name='password_change'),
        path('auth/change_password/done', auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'),
        path('auth/reset/init', auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset_init.html',
            email_template_name='auth/password_reset_email.html',
            subject_template_name='auth/password_reset_subject.txt'), name='password_reset'),
        path('auth/reset/done', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
        path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
        path('auth/reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
        path('auth/delete', views.delete_user, name='delete-user'),

        # PROFILE URLs
        path('profile', views.profile, name='profile'),
        path('profile/edit', views.edit_profile, name='edit_profile'),
        path('profile/export', views.export_profile, name='export_profile'),

        # BLOOD DONATION URLs
        path('add', views.add_donation, name='add-donation'),
        path('edit/<donation_id>', views.edit_donation, name='edit-donation'),
        path('drop/<donation_id>', views.drop_donation, name='drop-donation'),

        path('invite', views.invite, name='invite'),
        path('faq', views.faq, name='faq'),
        path('privacy', views.privacy, name='privacy'),
        path('places/add', views.add_donation_place, name='add-donation-place'),
        path('news', views.news, name='news'),
    ]
