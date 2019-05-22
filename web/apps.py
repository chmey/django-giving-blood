from django.apps import AppConfig


class WebConfig(AppConfig):
    name = 'web'
    # TODO: change me to an actual domain
    from_email_invite = 'invite@bloody-django.org'
