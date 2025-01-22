from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Sender(BaseModel):
    class SenderType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", _("Individual")
        ORGANIZATION = "ORGANIZATION", _("Organization")

    ledger = models.OneToOneField("ledgers.Ledger", on_delete=models.CASCADE, related_name="sender")
    sender_name = models.CharField(max_length=200, null=True, blank=True)
    sender_phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    sender_email = models.EmailField(max_length=200, null=True, blank=True)
    sender_address = models.CharField(null=True, blank=True)
    sender_type = models.CharField(max_length=200, choices=SenderType.choices, default=SenderType.ORGANIZATION)

    def __str__(self):
        return f"{self.sender_name} - {self.sender_phone_number} - {self.sender_email}"

    class Meta:
        verbose_name = _("Sender")
        verbose_name_plural = _("Senders")
