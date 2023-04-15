from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.sale.models import SaleOrder

