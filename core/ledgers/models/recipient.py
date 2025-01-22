from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Recipient(BaseModel):
    ledger = models.OneToOneField("ledgers.Ledger", on_delete=models.CASCADE, related_name="recipient")
    recipient_name = models.CharField(max_length=200, null=True, blank=True)
    recipient_phone_number = models.CharField(max_length=200, null=True, blank=True)
    job_title = models.ForeignKey("departments.JobTitle", on_delete=models.PROTECT, null=True, blank=True)
    department = models.ForeignKey("departments.Department", on_delete=models.PROTECT, null=True, blank=True)
    sector = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.recipient_name} - {self.sector} - {self.department}"

    class Meta:
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")
