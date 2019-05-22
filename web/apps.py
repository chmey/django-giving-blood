from django.apps import AppConfig


class WebConfig(AppConfig):
    name = 'web'
    # TODO: change me to an actual domain
    from_email_invite = 'invite@bloody-django.org'
    from_email_admin = 'administration@bloody-django.org'
