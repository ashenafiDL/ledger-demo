from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models.carrier import Carrier
from .models.delivery import Delivery
from .models.document import Document
from .models.ledger import Ledger
from .models.ledger_sharing import LedgerSharing
from .models.metadata import Metadata
from .models.recipient import Recipient


class LedgerAdmin(ModelAdmin):
    list_display = [
        "ledger_subject",
        "ledger_type",
        "status",
        "pdf_view_link",
    ]
    ordering = [
        "-updated_at",
    ]

    fieldsets = (
        (
            "Ledger Info",
            {
                "fields": (
                    "ledger_subject",
                    "ledger_description",
                    "ledger_type",
                    "reference_number",
                    "deadline",
                    "category",
                    "tracking_number",
                ),
            },
        ),
        (
            "Additional Info",
            {
                "fields": (
                    "received_at",
                    "status",
                    "approved_by",
                    "approved_at",
                    "priority",
                ),
            },
        ),
    )

    def pdf_view_link(self, obj):
        if obj.ledger_pdf:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.ledger_pdf)
        return "-"

    pdf_view_link.short_description = "PDF Version"


admin.site.register(Ledger, LedgerAdmin)


class CarrierAdmin(ModelAdmin):
    list_display = [
        "ledger",
        "carrier_person_first_name",
        "carrier_person_middle_name",
        "carrier_type",
    ]

    fieldsets = (
        (
            "Carrier Info",
            {
                "fields": (
                    "carrier_person_first_name",
                    "carrier_person_middle_name",
                    "carrier_person_last_name",
                    "carrier_phone_number",
                ),
            },
        ),
        (
            "Aditional Info",
            {
                "fields": (
                    "carrier_type",
                    "carrier_organization_id",
                    "carrier_plate_number",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Carrier, CarrierAdmin)


class DeliveryAdmin(ModelAdmin):
    list_display = [
        "ledger",
        "delivery_organization",
        "delivery_status",
        "expected_delivery_date",
    ]

    fieldsets = (
        (
            "Delivery Info",
            {
                "fields": (
                    "delivery_channel",
                    "delivery_medium",
                    "delivery_organization",
                    # "tracking_number",
                    "delivery_status",
                    "expected_delivery_date",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Delivery, DeliveryAdmin)


class DocumentAdmin(ModelAdmin):
    list_display = [
        "ledger",
        "document_owner",
        "document_type",
    ]

    fieldsets = (
        (
            "Document Info",
            {
                "fields": (
                    "document_type",
                    "document_owner",
                ),
            },
        ),
        (
            "Attachment Info",
            {
                "fields": (
                    "letter",
                    "attachment",
                ),
            },
        ),
        (
            "Additional Info",
            {
                "fields": (
                    "external_reference_id",
                    "additional_message",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "updated_at", "letter", "attachment"]


admin.site.register(Document, DocumentAdmin)


class RecipientAdmin(ModelAdmin):
    list_display = [
        "recipient_name",
        "department",
        "sector",
    ]

    fieldsets = (
        (
            "Ledger Info",
            {
                "fields": ("ledger",),
            },
        ),
        (
            "Recipient Info",
            {
                "fields": (
                    "recipient_name",
                    "department",
                    "job_title",
                    "sector",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Recipient, RecipientAdmin)


class MetadataAdmin(ModelAdmin):
    list_display = [
        "ledger",
        "metadata_title",
        "metadata_author",
    ]

    fieldsets = (
        (
            "Metadata Info",
            {
                "fields": (
                    "metadata_title",
                    "metadata_description",
                    "metadata_author",
                    "metadata_dateCreated",
                    "metadata_lastModified",
                    "metadata_category",
                    "metadata_fileType",
                    "metadata_keywords",
                    "metadata_language",
                    "metadata_tags",
                    "metadata_status",
                    "metadata_confidentiality",
                    "metadata_version",
                    "metadata_source_system",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Metadata, MetadataAdmin)


class LedgerSharingAdmin(ModelAdmin):
    list_display = [
        "ledger",
        "shared_to",
        "shared_at",
    ]
    ordering = ["-shared_at"]
    search_fields = ["shared_to__email"]
    list_filter = ["shared_at"]
    fieldsets = (
        (
            "Sharing Info",
            {
                "fields": (
                    "ledger",
                    "shared_to",
                ),
            },
        ),
    )


admin.site.register(LedgerSharing, LedgerSharingAdmin)
