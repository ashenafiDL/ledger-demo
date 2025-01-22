from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel

User = get_user_model()


class Ledger(BaseModel):
    class LedgerType(models.TextChoices):
        INCOMING = "INCOMING", _("Incoming")
        OUTGOING = "OUTGOING", _("Outgoing")
        PERSONAL = "PERSONAL", _("Personal")

    class LedgerStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")
        COMPLETED = "COMPLETED", _("Completed")

    class LedgerPriority(models.TextChoices):
        HIGH = "HIGH", _("High")
        MEDIUM = "MEDIUM", _("Medium")
        LOW = "LOW", _("LOW")

    ledger_subject = models.CharField(max_length=200, null=True, blank=True)
    ledger_description = models.TextField(null=True, blank=True)
    ledger_type = models.CharField(max_length=200, choices=LedgerType.choices, default=LedgerType.INCOMING)
    received_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=LedgerStatus.choices, default=LedgerStatus.PENDING)
    approved_by = models.CharField(max_length=200, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    reference_number = models.CharField(max_length=200, null=True, blank=True)
    deadline = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    priority = models.CharField(max_length=200, choices=LedgerPriority, null=True, blank=True)
    tracking_number = models.CharField(max_length=200, null=True, blank=True)
    ledger_pdf = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.ledger_subject} - {self.status} - {self.priority}"

    class Meta:
        verbose_name = "Ledger"
        verbose_name_plural = "Ledgers"
        permissions = (
            ("can_view_ledger", "Can view ledger"),
            ("can_create_ledger", "Can create ledger"),
            ("can_edit_ledger", "Can edit ledger"),
            ("can_delete_ledger", "Can delete ledger"),
        )
