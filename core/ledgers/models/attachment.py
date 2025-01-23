from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


def attachment_directory_path(instance, filename):
    # Default path if the type cannot be determined
    return f"ledger/other/attachment/{filename}"


class Attachment(BaseModel):
    file = models.FileField(upload_to=attachment_directory_path)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=150)
    file_size = models.IntegerField()
    uploaded_by = models.ForeignKey(
        "users.Member",
        on_delete=models.CASCADE,
        related_name="%(class)s_attachment",
        verbose_name=_("Uploaded By"),
    )
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Description"))

    def clean(self):
        if not self.file:
            raise ValidationError(_("A file is required."))

    class Meta:
        verbose_name = "Ledger_Attachment"
        verbose_name_plural = "Ledger_Attachments"

    def __str__(self):
        return f"Attachment: {self.file_name} ({self.file_type})"


def letter_directory_path(instance, filename):
    # Default path if the type cannot be determined
    return f"ledger/other/letter/{filename}"


class LedgerDoumentAttachment(BaseModel):
    file = models.FileField(upload_to=letter_directory_path)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=150)
    file_size = models.IntegerField()
    uploaded_by = models.ForeignKey(
        "users.Member",
        on_delete=models.CASCADE,
        related_name="%(class)s_attachment",
        verbose_name=_("Uploaded By"),
    )
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Description"))

    def clean(self):
        if not self.file:
            raise ValidationError(_("A file is required."))

    class Meta:
        verbose_name = "Ledger_Dcoument_Attachment"
        verbose_name_plural = "Ledger_Document_Attachments"

    def __str__(self):
        return f"Letter Attachment: {self.file_name} ({self.file_type})"
