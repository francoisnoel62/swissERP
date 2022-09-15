from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import SaleOrder
from ..payment.models import Payment


@receiver(post_save, sender=Payment)
def check_sale_solde(sender, instance, created, **kwargs):
    if created and instance.sale_id.solde == 0:
        print(instance.sale_id.order_state)
        instance.sale_id.order_state = 'PD'
        print(instance.sale_id.order_state)


@receiver(post_save, sender=Payment)
def save_sale_after_paid(sender, instance, **kwargs):
    if instance.sale_id.order_state == 'PD':
        print("oui")
        instance.sale_id.save()
