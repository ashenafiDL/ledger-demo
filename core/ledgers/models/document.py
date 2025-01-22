from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel

from .attachment import Attachment, LedgerDoumentAttachment


class Document(BaseModel):
    class DocumentType(models.TextChoices):
        Letter = "Letter", _("Letter")
        Invoice = "Invoice", _("Invoice")
        Receipt = "Receipt", _("Receipt")
        Report = "Report", _("Report")
        Other = "Other", _("Other")

    ledger = models.OneToOneField("ledgers.Ledger", on_delete=models.CASCADE, related_name="document")
    document_owner = models.CharField(max_length=200, null=True, blank=True)
    additional_message = models.CharField(max_length=200, null=True, blank=True)
    letter = models.ManyToManyField(LedgerDoumentAttachment)
    attachment = models.ManyToManyField(Attachment, blank=True)
    document_type = models.CharField(max_length=200, choices=DocumentType, default=DocumentType.Letter)
    document_date = models.DateTimeField(null=True, blank=True)
    external_reference_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.document_owner}-{self.document_type}-{self.document_date}"

    class Meta:
        verbose_name = _("Ledger Document")
        verbose_name_plural = _("Ledger Documents")
