from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
from core.common.models import BaseModel

User = get_user_model()


def attachment_directory_path(instance, filename):
    # Default path if the type cannot be determined
    return f"ledger/other/attachment/{filename}"


class Attachment(BaseModel):
    file = models.FileField(upload_to=attachment_directory_path)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=150)
    file_size = models.IntegerField()
    uploaded_by = models.ForeignKey(
        User,
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
        User,
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


class Ledger(BaseModel):

    class LedgerStatus(models.TextChoices):
        PENDING = "PENDING", _("PENDING")
        APPROVED = "APPROVED", _("APPROVED")
        ARCHIVED = "ARCHIVED", _("ARCHIVED")
        DELIVERED = "DELIVERED", _("DELIVERED")
        IN_REVIEW = "IN_REVIEW", _("IN_REVIEW")

    class MetadataConfidenciaity(models.TextChoices):
        PUBLIC = "PUBLIC", _("PUBLIC")
        INTERNAL = "INTERNAL", _("INTERNAL")
        CONFIDENTIAL = "CONFIDENTIAL", _("CONFIDENTIAL")
        RESTRICTED = "RESTRICTED", _("RESTRICTED")

    class LedgerPriority(models.TextChoices):
        HIGH = "HIGH", _("HIGH")
        MEDIUM = "MEDIUM", _("MEDIUM")
        LOW = "LOW", _("LOW")

    sender_name= models.CharField(max_length=200, blank=True, null=True)
    sender_phone_number= models.CharField(max_length=200, blank=True, null=True)
    sender_email= models.CharField(max_length=200, blank=True, null=True)
    carrier_person_first_name= models.CharField(max_length=200, blank=True, null=True)
    carrier_person_middle_name= models.CharField(max_length=200, blank=True, null=True)
    carrier_phone_number= models.CharField(max_length=200, blank=True, null=True)
    letter = models.ManyToManyField(LedgerDoumentAttachment)
    attachment = models.ManyToManyField(Attachment, blank=True)
    ledger_subject= models.CharField(max_length=200, blank=True, null=True)
    tracking_number = models.SlugField(unique=True, blank=True, null=True)
    ledger_status = models.CharField(max_length=200, choices=LedgerStatus.choices, default=LedgerStatus.PENDING)

    recipient_name= models.CharField(max_length=200, blank=True, null=True)
    recipient_phone_number= models.CharField(max_length=200, blank=True, null=True)
    job_title = models.ForeignKey(
        "departments.JobTitle", on_delete=models.PROTECT, null=True, blank=True
    )
    department = models.ForeignKey(
        "departments.Department", on_delete=models.PROTECT, null=True, blank=True
    )
    written_at= models.CharField(max_length=200, blank=True, null=True)
    priority = models.CharField(max_length=200, choices=LedgerPriority, null=True, blank=True)

    metadata_keywords= models.CharField(max_length=200, blank=True, null=True)
    metadata_tags= models.CharField(max_length=200, blank=True, null=True)
    metadata_fileType= models.CharField(max_length=200, blank=True, null=True)

    metadata_confidentiality = models.CharField(
        max_length=200,
        choices=MetadataConfidenciaity.choices,
        null=True,
        blank=True,
    )
    ledger_pdf = models.URLField(null=True, blank=True)


class LedgerSharing(BaseModel):
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name="shared_ledger")
    shared_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_to_ledgers")
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_by_ledgers")
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ledger", "shared_to")

    def __str__(self):
        return f"Ledger {self.ledger.id} shared by {self.shared_by} to {self.shared_to}"
