from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Payment


@receiver(post_save, sender=Payment)
def check_sale_solde(sender, instance, created, **kwargs):
    if created and instance.sale_id.solde == 0:
        instance.sale_id.order_state = 'PD'
        instance.sale_id.save()