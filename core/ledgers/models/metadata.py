from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Metadata(BaseModel):
    class MetadataStatus(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        IN_REVIEW = "IN_REVIEW", _("In_Review")
        APPROVED = "APPROVED", _("Approved")
        ARCHIVED = "ARCHIVED", _("Archived")
        PUBLISHED = "PUBLISHED", _("Published")

    class MetadataConfidenciaity(models.TextChoices):
        PUBLIC = "PUBLIC", _("Public")
        INTERNAL = "INTERNAL", _("Internal")
        CONFIDENTIAL = "CONFIDENTIAL", _("Confidential")
        RESTRICTED = "RESTRICTED", _("Restricted")

    ledger = models.OneToOneField("ledgers.Ledger", on_delete=models.CASCADE, related_name="metadatas")
    metadata_title = models.CharField(max_length=200, null=True, blank=True)
    metadata_description = models.TextField(null=True, blank=True)
    metadata_author = models.CharField(max_length=200, null=True, blank=True)
    metadata_date_created = models.CharField(max_length=200, null=True, blank=True)
    metadata_last_modified = models.CharField(max_length=200, null=True, blank=True)
    metadata_category = models.CharField(max_length=200, null=True, blank=True)
    metadata_file_type = models.CharField(max_length=200, null=True, blank=True)
    metadata_keywords = models.CharField(max_length=200, null=True, blank=True)
    metadata_language = models.CharField(max_length=200, null=True, blank=True)
    metadata_tags = models.CharField(max_length=200, null=True, blank=True)
    metadata_status = models.CharField(max_length=200, choices=MetadataStatus.choices, null=True, blank=True)
    metadata_confidentiality = models.CharField(
        max_length=200,
        choices=MetadataConfidenciaity.choices,
        null=True,
        blank=True,
    )
    metadata_version = models.CharField(max_length=200, null=True, blank=True)
    metadata_source_system = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.metadata_tags}-{self.metadata_title} - {self.metadata_author}"

    class Meta:
        verbose_name = _("Metadata")
        verbose_name_plural = _("Metadatas")
