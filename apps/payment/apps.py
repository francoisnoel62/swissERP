from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'apps.payment'

    def ready(self):
        from . import signals
