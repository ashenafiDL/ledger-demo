from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Delivery(BaseModel):
    class DeliveryStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        STAMPED = "STAMPED", _("Stamped")
        DELIVERED = "DELIVERED", _("Delivered")

    ledger = models.OneToOneField("ledgers.Ledger", on_delete=models.CASCADE, related_name="delivery")

    delivery_medium = models.CharField(max_length=200, null=True, blank=True)
    delivery_channel = models.CharField(max_length=200, null=True, blank=True)
    delivery_organization = models.CharField(max_length=200, null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(max_length=200, choices=DeliveryStatus.choices, null=True, blank=True)

    def __str__(self):
        return f"{self.delivery_organization} - {self.delivery_status}"

    class Meta:
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")
